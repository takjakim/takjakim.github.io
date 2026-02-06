# frozen_string_literal: true

# Generate /tags/<tag>/ pages for the notes collection.

module Jekyll
  class TagsGenerator < Generator
    safe true
    priority :low

    def generate(site)
      notes = site.collections['notes']&.docs || []
      tag_map = Hash.new { |h, k| h[k] = [] }

      notes.each do |doc|
        next unless doc.data['tags'].is_a?(Array)

        doc.data['tags'].each do |tag|
          next if tag.nil? || tag.to_s.strip.empty?
          tag_map[tag.to_s] << doc
        end
      end

      tag_map.each do |tag, docs|
        site.pages << TagPage.new(site, tag, docs)
      end
    end
  end

  class TagPage < Page
    def initialize(site, tag, docs)
      super(site, site.source, File.join('tags', Utils.slugify(tag)), 'index.html')
      self.data['layout'] = 'tag'
      self.data['tag'] = tag

      # This is a generated page (no real source file on disk).
      # Provide a stable last_modified_at so plugins/sitemap don't try to stat a missing file.
      now = Time.now
      self.data['last_modified_at'] = now
      self.data['last_modified_at_timestamp'] = now.to_i

      self.data['items'] = docs.sort_by { |d| d.data['last_modified_at'] || d.data['date'] || Time.at(0) }.reverse.map do |d|
        {
          'title' => d.data['title'],
          'url' => d.url,
          'slug' => d.data['slug'] || d.basename_without_ext,
          'last_modified_at' => d.data['last_modified_at']
        }
      end
      self.data['title'] = "##{tag}"
    end
  end
end
