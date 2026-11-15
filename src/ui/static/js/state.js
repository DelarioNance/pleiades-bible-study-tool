// Used to control state because the select elements do not
// have a built-in way to track the selection before change.
export const currentSelections = {
  book: { value: null, name: null },
  chapter: { value: null, name: null },
  verse: { value: null, name: null },
  depth: { value: null, name: null },
};