function href(key) {
  return [key, '#' + key]
}

export function apiNameToPath(name, api) {
  for (const compname in api) {
    const comp = api[compname];
    if (compname === name) {
      return [href(compname)];
    }

    if (name in comp) {
      return [href(compname), href(name)];
    }
  }
}