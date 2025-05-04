// Types for Infocard Highlights

export type InfocardHighlight = {
  index: number;
  text: string;
  visualDescription: string;
  storyContext?: string;
  imageUrl?: string; // URL for the generated highlight image
  imageUrlWithText?: string; // URL for the generated highlight image with text overlay
  post_text?: string;
};

export type InfocardHighlightResponse = {
  highlights: InfocardHighlight[];
};
