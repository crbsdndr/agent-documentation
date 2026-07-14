---
name: message-actions
description: Message interaction skill for chatbot UI — covers editing past messages, branching conversations, regenerating AI responses with version history, and copying message content or code blocks.
---

# Message Actions Skill

## How Actions Appear

Actions appear below the message they belong to.
- **Desktop** — appears on hover
- **Mobile** — appears on tap

Actions disappear when the user moves away (desktop) or taps elsewhere (mobile).

**User message actions** — Edit, Delete, New Branch
**AI message actions** — Regenerate, Copy, Delete

## Edit Message

When the user edits a past message:
1. Show an inline text editor on the selected message
2. All messages after it are permanently removed
3. The edited message becomes the last message in the conversation
4. AI responds fresh from that point

## New Branch

When the user edits but wants to keep the original conversation:
1. Instead of replacing, create a new conversation branch from that message
2. The original thread stays intact and accessible
3. User can switch between branches — show a branch indicator on the branching point
4. Each branch is independent — editing one does not affect the other

## Regenerate

When the user asks AI to answer again:
1. AI generates a new response to replace the last one
2. The previous response is saved, not discarded
3. Show a navigation control (e.g. 1/2, 1/3) so the user can browse all versions
4. Only the last AI message can be regenerated — not messages in the middle of a conversation
5. Only the version currently viewed by the user is used as AI memory — not all versions

## Delete Message

When the user deletes a message:
1. Ask for confirmation first — use whatever confirmation pattern the codebase already has (modal, dialog, inline prompt, etc.)
2. If confirmed, remove the message and all messages after it permanently
3. If cancelled, do nothing

When the user copies a message:
1. Entire message — copy raw markdown as-is
2. Code block — each code block has its own copy button, copies only that block
3. Show a brief confirmation (e.g. checkmark) after copying so the user knows it worked
4. On mobile, allow native text selection via long-press and drag to select specific parts of a message

## Copy

When the user copies a message:
1. Entire message — copy raw markdown as-is
2. Code block — each code block has its own copy button, copies only that block
3. Show a brief confirmation (e.g. checkmark) after copying so the user knows it worked
4. On mobile, allow native text selection via long-press and drag to select specific parts of a message