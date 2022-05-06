# Changelog


## Unreleased


## 1.1.0
### Added
- python 3.10 support
### Fixed
- made migrations idempotent for ASNs (#14)
### Removed
- python 3.6 support


## 1.0.1
### Fixed
- alias for original rest.IPPrefixField


## 1.0.0
### Added
- support for python up to 3.9
- support for django-3.2
### Changed
- IPPrefixField to IPNetworkField
### Removed
- support for python <3.6
- support for django <2.2


## 0.5.0
### Added
- django 3.0 support


## 0.4.0
### Added
- django 2.0, 2.2 support
### Changed
- move to ctl for package/release management


## 0.3.2
### Fixed
- fix validator meta corruption


## 0.3.1
### Fixed
- IPPrefixValidator overwriting all field meta


## 0.3.0
### Added
- python 3 support
- django 1.10 support
- better tests
### Deprecated
- URLField


## 0.2.0
### Added
- test stubs
### Fixed
- correct requirements