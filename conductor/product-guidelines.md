# Product Guidelines: AI Mafia

## Visual Identity

### Theme: Playful & Colorful
AI Mafia embraces a vibrant, fun, and energetic visual identity that reflects its nature as a casual party game. The design should feel inviting, lighthearted, and immediately communicate "fun with friends."

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Primary | Vivid Purple | `#7C3AED` | Buttons, active states, primary actions |
| Secondary | Hot Pink | `#EC4899` | Accents, highlights, AI-related elements |
| Success | Emerald Green | `#10B981` | Connected status, correct actions, human win |
| Danger | Coral Red | `#F43F5E` | Voting, elimination, AI win |
| Warning | Amber | `#F59E0B` | Timers, countdowns, alerts |
| Background | Soft White | `#F8FAFC` | Main background |
| Surface | Light Gray | `#F1F5F9` | Cards, panels, chat bubbles |
| Text Primary | Dark Slate | `#1E293B` | Headings, body text |
| Text Secondary | Medium Gray | `#64748B` | Captions, metadata |

### Typography
- **Headings:** Bold, rounded sans-serif font (e.g., Nunito, Poppins) to convey friendliness
- **Body:** Clean, readable sans-serif (e.g., Inter, Open Sans)
- **Chat messages:** Slightly smaller, comfortable reading size for rapid scanning
- **Game status text:** Large, bold, high-contrast for at-a-glance readability

### Iconography & Illustration
- Use rounded, friendly icons with consistent stroke width
- Incorporate playful illustrations for game states (e.g., magnifying glass for detective mode, speech bubbles for chat)
- Emoji-style visual cues are welcome to reinforce the casual tone
- Voting phase should use visually distinct, attention-grabbing indicators

### Shape Language
- **Border radius:** Generous rounding on all interactive elements (12-16px for cards, fully rounded for buttons and avatars)
- **Shadows:** Soft, diffused shadows for depth without heaviness
- **Spacing:** Comfortable, breathable layouts with clear visual hierarchy

## Animation & Motion

### Principles
- Animations should be snappy and delightful, not slow and dramatic
- Use bouncy easing (ease-out, spring) rather than linear motion
- Keep transitions under 300ms for interactive elements
- Reserve longer animations (500ms+) for state changes (e.g., phase transitions, eliminations)

### Key Animations
- **Turn indicator:** Smooth, attention-drawing animation when it's a player's turn to speak
- **Timer countdown:** Visible, pulsing countdown that creates urgency without anxiety
- **Vote reveal:** Satisfying reveal animation showing vote tallies
- **Elimination:** Dramatic but brief animation when a player is voted out
- **Win/Lose:** Celebratory or dramatic full-screen animation for game end

## Tone & Voice

### Writing Style
- **Casual and conversational** -- write like you're talking to a friend
- **Encouraging and energetic** -- use active voice and action-oriented language
- **Brief and punchy** -- keep UI text short; every word should earn its place
- **Playful humor** -- light jokes and witty microcopy are encouraged

### Examples
| Context | Good | Avoid |
|---|---|---|
| Join prompt | "What's your name, detective?" | "Enter your username" |
| Game start | "The hunt begins!" | "Game has started" |
| Your turn | "Your turn! Say something..." | "You may now type a message" |
| Time running out | "Hurry up! 5s left!" | "5 seconds remaining" |
| Elimination | "Alex has been voted out!" | "Player Alex eliminated" |
| AI caught | "You found the impostor!" | "AI agent identified" |
| AI wins | "The AI fooled everyone!" | "AI wins the game" |

### Language
- Support both English and Traditional Chinese (zh-TW)
- UI labels and game messages should be localized
- Player-generated content (chat messages, names) remains as-is

## Responsive Design

### Mobile-First Approach
- Touch targets minimum 44x44px
- Chat interface should be thumb-friendly with input at the bottom
- Voting cards should be large enough to tap comfortably
- Timer and game status always visible without scrolling

### Breakpoints
- **Mobile:** < 640px (primary design target)
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

## Accessibility

- Minimum contrast ratio of 4.5:1 for body text, 3:1 for large text
- All interactive elements must be keyboard-navigable
- Screen reader support for game state changes and turn notifications
- Color should not be the only indicator of state (use icons and text labels alongside)
- Timer should have both visual and optional audio cues
