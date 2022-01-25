require 'json'

metadata = JSON.parse(IO.read(File.expand_path('../../shared_metadata.json', __FILE__)))

Gem::Specification.new do |spec|
  spec.name          = "kalibera"
  spec.version       = metadata["metadata"]["version"].to_s + ".2"
  spec.authors       = ["Edd Barrett", "Carl Friedrich Bolz", "Chris Seaton"]
  spec.email         = ["chris@chrisseaton.com"]
  spec.summary       = metadata["metadata"]["short_descr"]
  spec.description   = metadata["metadata"]["long_descr"]
  spec.homepage      = metadata["metadata"]["url"]
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0")
  spec.test_files    = spec.files.grep(%r{^test/})
  spec.require_paths = ["lib"]

  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "test-unit", "~> 3.4"

  spec.add_dependency "rbzip2", "~> 0.3"
  spec.add_dependency "memoist", "~> 0.16"
end
