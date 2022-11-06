function href(key) {
  return [key, '#' + key]
}

export function apiNameToPathHref(name, api) {
  return apiNameToPath(name, api).map(href);
}

export function apiNameToPath(name, api) {
  for (const compname in api) {
    const comp = api[compname];
    if (compname === name) {
      return [compname];
    }

    if (name in comp) {
      return [compname, name];
    }
  }
  return [];
}