# frozen_string_literal: true

require 'date'
require 'time'

module HomeRecommendations
  # Build the home page recommendation rail from a small manual pin list plus
  # dynamic signals: importance, featured flag, pageviews, and recency.
  class Generator < Jekyll::Generator
    priority :low

    def generate(site)
      notes = site.collections['notes']&.docs || []
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

      site.data['home_recommendations'] = selected.first(limit)
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

    def normalize_url(url)
      normalized = url.to_s
      normalized = "/#{normalized}" unless normalized.start_with?('/')
      normalized = "#{normalized}/" unless normalized.end_with?('/')
      normalized
    end
  end
end
