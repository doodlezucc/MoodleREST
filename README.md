# Moodle Web Service API Reference

An unofficial, automatically generated API reference for [Moodle](https://docs.moodle.org/dev/Creating_a_web_service_client) web services.


## Generating the Reference

Download the latest [Moodle release](https://download.moodle.org/releases/latest/) and run the server. Open your browser and navigate to _http://localhost:80_ to create a local admin account and install all components of the Moodle platform. Activate web services in the [Advanced features](http://localhost:80/admin/settings.php?section=optionalsubsystems) section (make sure to save changes).

Move the extraction script [scripts/doc_json.php](https://github.com/doodlezucc/MoodleREST/blob/master/scripts/doc_json.php) into `<MOODLE ROOT>/server/moodle/`. On your hosted Moodle website, 

### Development (PHP Script)

If you're trying to make changes to the PHP script, it's helpful to disable caching. Open `server/php/php.ini` and scroll to the bottom of the file to find cache related settings. Edit _opcache.enable_ to have a value of `0` and (re-)start your Moodle server.
```ini
opcache.enable=0
```

Debug messages are another helpful setting and can be enabled in [Development > Debugging](http://localhost:80/admin/settings.php?section=debugging). Check the _Display debug messages_ setting to view warnings and errors in the browser (otherwise, they'd appear in `server/apache/logs/error.log`).


### Output Format

The generated JSON files follow a custom schema _inspired_ by OpenAPI.
Moodle's web service functions all have separate _IDs_ passed to a single `server.php` endpoint path. Because there's only one endpoint, the standard OpenAPI schema can't be used for Moodle web services.
