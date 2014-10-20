# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'kalibera/version'

Gem::Specification.new do |spec|
  spec.name          = "kalibera"
  spec.version       = Kalibera::VERSION
  spec.authors       = ["Edd Barrett", "Carl Friedrich Bolz", "Chris Seaton"]
  spec.email         = ["chris@chrisseaton.com"]
  spec.summary       = %q{An implementation of Tomas Kalibera's statistically rigorous benchmarking method.}
  spec.description   = %q{An implementation of Tomas Kalibera's statistically rigorous benchmarking method.}
  spec.homepage      = ""
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0")
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.test_files    = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths = ["lib"]

  spec.add_development_dependency "bundler", "~> 1.7"
  spec.add_development_dependency "rake", "~> 10.0"

  spec.add_dependency "rbzip2", "~> 0.2.0"
  spec.add_dependency "memoist", "~> 0.11.0"
end
