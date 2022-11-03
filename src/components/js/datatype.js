export default function simpleType(type) {
  switch (type) {
    case "int":
    case "float":
      return "number";
    case "bool":
    case "object":
    case "array":
      return type;
    default:
      return "string";
  }
}
