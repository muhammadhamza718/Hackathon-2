/**
 * Type declarations for OpenAI ChatKit Web Component
 * This file declares the custom element for TypeScript/JSX compatibility
 */

declare namespace JSX {
  interface IntrinsicElements {
    "openai-chatkit": React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & {
        ref?: React.Ref<any>;
        class?: string;
      },
      HTMLElement
    >;
  }
}
