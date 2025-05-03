// Types for Infocard Highlights

export type InfocardHighlight = {
  index: number;
  text: string;
  visualDescription: string;
  storyContext?: string;
  image_url?: string; // URL for the generated highlight image
};

export type InfocardHighlightResponse = {
  highlights: InfocardHighlight[];
};
