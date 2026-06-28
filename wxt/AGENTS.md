# AGENTS.md - WXT

## Entrypoints and Build Output

* Must use WXT entrypoints for extension surfaces.
* Must configure extension behavior through WXT source files.
* Must not edit generated files inside `.output` or `.wxt`.
* Must avoid browser and extension API calls at entrypoint module top level.

## Extension Boundaries

* Must keep host-page DOM interaction inside content scripts.
* Must keep extension lifecycle and extension-wide event listeners inside the background entrypoint.
* Must use explicit messages for direct work between extension surfaces.
* Must define and validate message payloads before acting on them.

## Content Scripts

* Must make repeated execution safe and avoid duplicate page changes.
* Must use stable selectors for host-page interaction.
* Must clean up resources created by the content script.
* Must keep host-page-specific behavior separate from reusable extension logic.
* Must resolve extension assets to extension URLs before loading them from a content script.

## Permissions and Manifest

* Must keep permissions, host access, and match patterns limited to the feature’s actual needs.
* Must add `web_accessible_resources` only for assets that a webpage needs to load.

## Verification

* Must run the project’s configured WXT build command after changing entrypoints, WXT configuration, manifest behavior, or bundled assets.
* Must verify affected extension flows after runtime behavior changes.
