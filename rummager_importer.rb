require_relative "service"
require "csv"
require 'pry'

module Import
  class RummagerImporter
    def import
      output = CSV.new($stdout)
      CSV.foreach('audits.csv', headers: true) do |row|
        link = row["Link"].strip
        begin
          uri = URI(link)
        rescue URI::InvalidURIError
          $stderr.puts "Bad URI: #{link}"
          next
        end

        next if link == ""

        audit = row["Audit"]
        response = do_request(link_to_base_path(link))

        while response.nil?
          redirect = try_redirect(uri)
          if redirect.nil?
            $stderr.puts "Skipping #{link}" # No search data or redirect found
            break
          end

          response = do_request(link_to_base_path(redirect))
        end

        unless response.nil?
          output << [link, audit, response["indexable_content"], response["is_withdrawn"]]
        end
      end
    end

  private

    def try_redirect(uri)
      response = Net::HTTP.get_response(uri)
      case response
      when Net::HTTPRedirection then
        response['location']
        $stderr.puts "Found redirected content #{uri} -> #{response['location']}"
      else
        nil
      end
    end

    def link_to_base_path(link)
      link.gsub(/https?:\/\/www.gov.uk/, "")
    end

    def do_request(link)
      Services.rummager.unified_search(
        fields: %w(link content_id format mainstream_browse_pages specialist_sectors organisations policy_groups people policy_areas taxons indexable_content is_withdrawn),
        filter_link: link,
        debug: "include_withdrawn"
      ).results.first
    end
  end
end

Import::RummagerImporter.new.import
