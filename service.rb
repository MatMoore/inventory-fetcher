require "gds_api/rummager"

module Services
  def self.rummager
    @rummager ||= with_retries(
      GdsApi::Rummager.new(Plek.new.find('rummager'),
        timeout: 20,
        disable_cache: true,
    ))
  end

  def self.with_retries(target)
    RetryWrapper.new(target: target, maximum_number_of_attempts: 5)
  end

  class RetryWrapper
    def initialize(target:, maximum_number_of_attempts:)
      @target = target
      @maximum_number_of_attempts = maximum_number_of_attempts
    end

    def method_missing(method_sym, *arguments, &block)
      attempts = 0
      begin
        attempts += 1
        @target.public_send(method_sym, *arguments, &block)
      rescue Timeout::Error, GdsApi::TimedOutException, GdsApi::HTTPServerError => e
        raise e if attempts >= @maximum_number_of_attempts
        sleep sleep_time_after_attempt(attempts)
        retry
      end
    end

    def sleep_time_after_attempt(current_attempt)
      current_attempt
    end
  end
end
