// Utility for deep updating nested objects by path
export function setIn<T>(obj: T, path: string[], value: any): T {
  if (path.length === 0) return obj;
  const [head, ...rest] = path;
  return {
    ...obj,
    [head]: rest.length
      ? setIn((obj as any)[head] || {}, rest, value)
      : value,
  };
}
