/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the authoring server for the overlay's links; "" hides them (D-35). */
  readonly VITE_AUTHORING_URL?: string;
}
