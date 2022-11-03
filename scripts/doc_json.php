<?php

/**
 * This file is meant to be copied to your Moodle directory (/server/moodle/doc_json.php).
 * Once your Moodle process is running, navigate to http://localhost:80/doc_json.php to
 * generate all webservice endpoints and write them to "wsapi.json".
 * 
 * 
 * >> EXTRA STEP: NULLABLE PARAMETERS <<
 * 
 * To better detect nullable parameters in service functions, the constructor of
 * Moodle's external_value class (located in "/server/moodle/lib/externallib.php")
 * should be changed. The relevant lines look like this in Moodle 4.0.0:
 * 
 *     620   class external_value extends external_description {
 *    [...]
 *     638      public function __construct($type, $desc='', $required=VALUE_REQUIRED,
 *     639              $default=null, $allownull=NULL_ALLOWED) {
 *    [...]
 * 
 * As you can see, external_value's constructor sets $allownull to NULL_ALLOWED by default.
 * This is bad because $allownull seems to get explicitly passed in only 50% of all functions.
 * The other half of functions don't specify any nullability of accepted parameters.
 * 
 * In order to extract a more accurate API, replace "NULL_ALLOWED" with "null" ($allownull=null).
 * The extraction script differentiates between three possible values "true", "false" and "null"
 * when reading $allownull and only adds "nullable: true|false" to the JSON entry if it's boolean.
 */

require_once('./config.php');
require($CFG->dirroot . '/webservice/lib.php');

function describe($params, $includeRequired)
{
    if (!is_object($params)) {
        return null;
    }

    $result = new stdClass();
    if ($params->desc != null) {
        $result->description = $params->desc;
    }
    $result->type = "undefined";

    if ($params instanceof external_multiple_structure) {
        // description object is a list
        $type = "array";
        $result->items = describe($params->content, $includeRequired);
    } else if ($params instanceof external_single_structure) {
        // description object is an object
        $type = "object";
        $result->properties = new stdClass();

        foreach ($params->keys as $attributname => $attribut) {
            $result->properties->{$attributname} = describe($attribut, $includeRequired);
        }
    } else {
        $type = $params->type;
    }

    $result->type = $type;

    if (property_exists($params, "allownull") && is_bool($params->allownull)) {
        $result->nullable = $params->allownull;
    }
    if ($includeRequired) {
        if ($params->required == VALUE_REQUIRED) {
            $result->required = true;
        }
        if ($params->required == VALUE_DEFAULT) {
            $result->default = $params->default;
        }
    }
    return $result;
}

function fn_to_object($spec, $convert = true)
{
    $description = external_api::external_function_info($spec);
    if (!$convert) {
        return $description;
    }

    $params = new stdClass();

    foreach ($description->parameters_desc->keys as $paramname => $paramdesc) {
        $param = describe($paramdesc, true);

        $params->{$paramname} = $param;
    }

    $return_desc = $description->returns_desc;

    if (is_object($return_desc)) {
        $returns = describe($return_desc, false);
    } else {
        $returns = null;
    }

    return (object) [
        "id" => $spec->id,
        "description" => $description->description,
        "request" => $params,
        "response" => $returns,
        "requiresLogin" => $description->loginrequired,
        "ajaxAllowed" => $description->allowed_from_ajax,
        "services" => $description->services,
    ];
}

/**
 * Adds a computed entry to the output array `arr`.
 * The function's component is used as top layer key.
 */
function insert_function($function, &$arr, $convert = true)
{
    $desc = fn_to_object($function, $convert);

    $key = $function->component;
    if (!array_key_exists($key, $arr)) {
        $arr[$key] = array();
    }

    $arr[$key][$function->name] = $desc;
}

function fullpage_textarea($content)
{
    return html_writer::tag("textarea", $content, array("style" => "width: 100%; min-height: 100%;"));
}

/**
 * Returns a full page textarea filled with the contents of `obj` in JSON format.
 */
function to_json($obj, $prettyprint = true)
{
    $flags = JSON_UNESCAPED_SLASHES;
    if ($prettyprint) {
        $flags |= JSON_PRETTY_PRINT;
    }

    $content = json_encode($obj, $flags);
    return $content;
}

$functions = $DB->get_records('external_functions', array(), 'name');
$functiondescs = array();
$select = 15;
foreach ($functions as $function) {
    $select--;
    if (true || $select == 0) {
        insert_function($function, $functiondescs);
    }
}

/// OUTPUT
$result = to_json($functiondescs, false);
file_put_contents("wsapi.json", $result);
echo fullpage_textarea($result);
