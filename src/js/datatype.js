import paramTypes from "../api/params.json";

export function simpleType(type) {
  switch (type) {
    case "int":
    case "float":
      return "number";
    case "bool":
    case "object":
    case "array":
      return type;
    case "timezone":
      return "timezone";
    default:
      return "string";
  }
}

export function typeDescription(type) {
  return paramTypes[type];
}