# frozen_string_literal: true

require 'date'
require 'time'
require 'digest'

module HomeRecommendations
  # Build the home page recommendation rail from a small manual pin list plus
  # dynamic signals: importance, featured flag, pageviews, and recency.
  class Generator < Jekyll::Generator
    priority :low

    def generate(site)
      all_docs = site.collections['notes']&.docs || []
      notes = all_docs.reject { |doc| concept_note?(doc) }
      home_config = site.data['home'] || {}
      featured_config = home_config['featured'] || {}
      limit = (featured_config['limit'] || 3).to_i
      recent_days = (featured_config['recent_days'] || 45).to_i
      pinned_urls = Array(featured_config['pinned']).map { |url| normalize_url(url) }
      pageviews = site.data.dig('pageviews', 'paths') || {}

      docs_by_url = notes.each_with_object({}) do |doc, memo|
        memo[normalize_url(doc.url)] = doc
      end

      pinned_items = pinned_urls.filter_map do |url|
        doc = docs_by_url[url]
        next unless doc

        build_item(doc, pageviews, reason: '고정', pinned: true, recent_days: recent_days)
      end

      pinned_lookup = pinned_items.map { |item| normalize_url(item['url']) }
      candidates = notes
                   .reject { |doc| pinned_lookup.include?(normalize_url(doc.url)) }
                   .map { |doc| build_item(doc, pageviews, recent_days: recent_days) }
                   .sort_by { |item| [-item['score'], -item['timestamp']] }

      selected = pinned_items.first(limit)
      remaining_slots = limit - selected.size
      if remaining_slots.positive?
        selected.concat(diversified_pick(candidates, remaining_slots, selected))
      end

      selected = selected.first(limit)
      site.data['home_recommendations'] = selected
      site.data['home_recommendations_graph'] = build_recommendation_graph(selected, all_docs)
    end

    private

    def diversified_pick(candidates, limit, already_selected)
      picked = []
      used_categories = already_selected.map { |item| item['category'] }.compact

      candidates.each do |item|
        break if picked.size >= limit
        next if used_categories.include?(item['category'])

        picked << item
        used_categories << item['category']
      end

      if picked.size < limit
        picked_urls = picked.map { |item| item['url'] }
        candidates.each do |item|
          break if picked.size >= limit
          next if picked_urls.include?(item['url'])

          picked << item
          picked_urls << item['url']
        end
      end

      picked
    end

    def build_item(doc, pageviews, reason: nil, pinned: false, recent_days: 45)
      url = normalize_url(doc.url)
      modified_time = modified_time_for(doc)
      views = pageviews.dig(url, 'views').to_i
      importance = doc.data.fetch('importance', 1).to_i
      featured = doc.data['featured'] == true
      age_days = [(Time.now - modified_time) / 86_400, 0].max
      recency_bonus = recency_bonus(age_days, recent_days)
      score = importance * 20 + views * 4 + recency_bonus
      score += 15 if featured
      score -= 25 if age_days > 120 && views < 5
      score += 1000 if pinned

      {
        'title' => doc.data['title'] || doc.basename_without_ext,
        'url' => url,
        'category' => category_for(doc),
        'label' => doc.data['label'],
        'date_label' => modified_time.strftime('%m.%d'),
        'timestamp' => modified_time.to_i,
        'views' => views,
        'excerpt' => excerpt_for(doc),
        'score' => score.round(2),
        'reason' => reason || reason_for(featured, views, age_days, recent_days)
      }
    end

    def modified_time_for(doc)
      raw = doc.data['last_modified_at_timestamp'] || doc.data['last_modified_at'] || doc.data['date']
      case raw
      when Time
        raw
      when Date
        raw.to_time
      when nil
        Time.at(0)
      else
        Time.parse(raw.to_s)
      end
    rescue StandardError
      Time.at(0)
    end

    def category_for(doc)
      parts = doc.relative_path.split('/')
      parts[1] || 'note'
    end

    def excerpt_for(doc)
      description = doc.data['description']
      return description.to_s.strip if description && !description.to_s.strip.empty?

      doc.content
         .gsub(/```.*?```/m, ' ')
         .gsub(/<[^>]*>/, ' ')
         .gsub(/[#>*_`\[\]()|-]/, ' ')
         .gsub(/\s+/, ' ')
         .strip
    end

    def reason_for(featured, views, age_days, recent_days)
      return '큐레이션' if featured
      return '인기' if views >= 5
      return '최근' if age_days <= recent_days

      '추천'
    end

    def recency_bonus(age_days, recent_days)
      return 80 if age_days <= 7
      return 50 if age_days <= recent_days
      return 15 if age_days <= 120

      0
    end

    def concept_note?(doc)
      doc.data['type'].to_s == 'concept' || doc.data['hide_from_recent'] == true
    end

    def normalize_url(url)
      normalized = url.to_s
      normalized = "/#{normalized}" unless normalized.start_with?('/')
      normalized = "#{normalized}/" unless normalized.end_with?('/')
      normalized
    end

    def build_recommendation_graph(selected_items, all_docs)
      return { 'nodes' => [], 'edges' => [] } if selected_items.empty?

      docs_by_url = all_docs.each_with_object({}) { |doc, memo| memo[normalize_url(doc.url)] = doc }
      docs_by_title = all_docs.each_with_object({}) do |doc, memo|
        title = doc.data['title'].to_s.strip
        memo[title] = doc unless title.empty?
        memo[doc.basename_without_ext.to_s] = doc
      end

      nodes = []
      edges = []
      seen = {}

      selected_docs = selected_items.filter_map { |item| docs_by_url[normalize_url(item['url'])] }
      selected_docs.each_with_index do |doc, index|
        add_graph_node(nodes, seen, doc, 'featured', selected_items[index]&.dig('reason'))
      end

      linked_docs = []
      selected_docs.each do |source|
        wiki_targets(source.content).each do |target|
          target_doc = docs_by_title[target]
          next unless target_doc
          next if normalize_url(target_doc.url) == normalize_url(source.url)

          add_graph_node(nodes, seen, target_doc, concept_note?(target_doc) ? 'concept' : 'note', nil)
          edge_id = "#{normalize_url(source.url)}->#{normalize_url(target_doc.url)}"
          edges << { 'source' => node_id(source), 'target' => node_id(target_doc) } unless linked_docs.include?(edge_id)
          linked_docs << edge_id
          break if nodes.size >= 12
        end
        break if nodes.size >= 12
      end

      position_graph_nodes(nodes)
      { 'nodes' => nodes, 'edges' => edges }
    end

    def wiki_targets(content)
      content.to_s.scan(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/).flatten.map(&:strip).uniq
    end

    def add_graph_node(nodes, seen, doc, kind, reason)
      id = node_id(doc)
      return if seen[id]

      seen[id] = true
      nodes << {
        'id' => id,
        'title' => doc.data['title'] || doc.basename_without_ext,
        'url' => normalize_url(doc.url),
        'category' => category_for(doc),
        'kind' => kind,
        'reason' => reason
      }
    end

    def node_id(doc)
      Digest::SHA1.hexdigest(normalize_url(doc.url))[0, 10]
    end

    def position_graph_nodes(nodes)
      return nodes if nodes.empty?

      featured = nodes.select { |node| node['kind'] == 'featured' }
      related = nodes.reject { |node| node['kind'] == 'featured' }

      featured.each_with_index do |node, index|
        node['x'] = 120 + index * 92
        node['y'] = 92 + (index % 2) * 78
      end

      related.each_with_index do |node, index|
        angle = (Math::PI * 2 * index / [related.size, 1].max) - Math::PI / 2
        node['x'] = (300 + Math.cos(angle) * 158).round
        node['y'] = (142 + Math.sin(angle) * 96).round
      end

      nodes
    end
  end
end
