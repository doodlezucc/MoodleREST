# Moodle Web Service API Reference

An unofficial, automatically generated API reference for [Moodle](https://docs.moodle.org/dev/Creating_a_web_service_client) web services.

## JSON Format

The generated JSON files follow a custom schema _inspired_ by OpenAPI.
Moodle's web service functions all have separate _IDs_ passed to a single `server.php` endpoint path. Because there's only one endpoint, the standard OpenAPI schema can't be used for Moodle web services.
