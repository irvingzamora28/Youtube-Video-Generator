// Types for Infocard Highlights

export type InfocardHighlight = {
  index: number;
  text: string;
  visualDescription: string;
  storyContext?: string;
};

export type InfocardHighlightResponse = {
  highlights: InfocardHighlight[];
};
