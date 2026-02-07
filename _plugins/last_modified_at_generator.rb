# frozen_string_literal: true

require 'fileutils'
require 'pathname'
require 'jekyll-last-modified-at'

module Recents
  # Generate change information for all markdown pages
  class Generator < Jekyll::Generator
    def generate(site)
      items = site.collections['notes'].docs
      items.each do |page|
        # front matter의 last_modified_at 값이 있으면 우선 사용
        if page.data['last_modified_at']
          # front matter 값을 ISO 8601 형식으로 변환
          fm_date = page.data['last_modified_at']
          timestamp = if fm_date.is_a?(Time) || fm_date.is_a?(Date)
                        fm_date.strftime('%FT%T%:z')
                      else
                        # 문자열인 경우 파싱 후 변환
                        Time.parse(fm_date.to_s).strftime('%FT%T%:z')
                      end
        else
          # front matter 값이 없으면 git/파일 시간 사용
          timestamp = Jekyll::LastModifiedAt::Determinator.new(site.source, page.path, '%FT%T%:z').to_s
        end
        page.data['last_modified_at_timestamp'] = timestamp
      end
    end
  end
end
