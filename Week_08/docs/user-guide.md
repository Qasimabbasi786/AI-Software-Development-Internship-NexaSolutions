# User Guide: Nexa Solutions AI Library Assistant

**Welcome to the Nexa Solutions Library Assistant!**  
This guide explains what the AI assistant can do, how human-in-the-loop approvals safeguard your account, and how your privacy and data are protected.

---

## 1. What Can the Assistant Do?

The Library Assistant is an intelligent companion designed to help you discover, evaluate, and reserve books from the catalog.

### Key Capabilities:
- **Natural Language Catalog Search:** Ask questions in plain English or other languages (e.g. *"Find science fiction books about space exploration"* or *"Which books cover distributed transactions?"*).
- **Real-Time Availability Inquiries:** Inquire whether specific titles are currently on the shelf or checked out (e.g. *"Is Clean Code available to borrow?"*).
- **Context-Aware Recommendations:** Ask for suggestions based on topic, author, or difficulty level (e.g. *"I enjoyed Designing Data-Intensive Applications, what should I read next?"*).
- **Direct Book Reservations:** Instruct the assistant to place a hold or reservation on an available book.
- **Active Reservation Tracking:** Check your current loans and pending holds (e.g. *"Show my active reservations"*).

---

## 2. Interactive Human-in-the-Loop (HITL) Approvals

To ensure your account is protected against accidental bookings, mistaken book selections, or unintended automated actions, **the assistant is strictly forbidden from reserving books without your explicit permission.**

### How the Approval Card Works:
1. When you instruct the assistant: *"Please reserve Dune for me"*, the assistant locates the book and verifies its status.
2. Instead of immediately reserving the title, the assistant **pauses** execution and displays an **Approval Card** in the chat drawer:
   ```
   ┌────────────────────────────────────────────────────────┐
   │ 📖 Action Approval Required                            │
   │ The assistant requests permission to perform:           │
   │ • Action: Reserve Book                                 │
   │ • Title: Dune (Frank Herbert) - Book ID: 4             │
   │ • Borrower: demo_user                                  │
   │                                                        │
   │ [ ✅ Approve & Reserve ]       [ ❌ Cancel / Reject ]   │
   └────────────────────────────────────────────────────────┘
   ```
3. **If you click [Approve & Reserve]:** The reservation is processed against the library database, assigning you a unique confirmation number.
4. **If you click [Cancel / Reject]:** The action is aborted instantly. No records are written to the database.

---

## 3. Data Storage & Privacy Policies

### What Information We Store:
- **User Account:** Your username, hashed password, and role.
- **Active Reservations:** Records of books you have reserved or borrowed.
- **Preferences:** Optional reading interests or notification settings you save.
- **Conversation State:** Short-term chat history stored securely in an isolated session checkpointer so multi-turn conversations maintain context.

### What We NEVER Store:
- We never store or log your plaintext passwords, payment info, or full LLM authentication tokens.

---

## 4. How to Delete Your Data (GDPR "Right to be Forgotten")

In accordance with international privacy regulations (GDPR and CCPA), you have full control over your personal data.

### Requesting Immediate Data Erasure:
You can purge all your account information, reservation history, reading preferences, and AI conversation checkpoints:

1. **Via the Web Interface:**
   - Navigate to **User Profile / Settings**.
   - Scroll down to the **Data Privacy & Erasure** panel.
   - Click **"Delete My Account & Personal Data"** and confirm.
2. **Via Direct API Request:**
   ```bash
   curl -X DELETE "http://localhost:5000/api/users/{your_user_id}/data" \
        -H "Authorization: Bearer <your_jwt_token>"
   ```

### What Happens When You Request Deletion?
- Your user profile and account credentials are permanently deleted from PostgreSQL.
- All historical reservation and preference records are removed.
- All LangGraph AI conversation checkpoints and memory threads associated with your user ID are purged from the SQLite checkpointer.
- The operation is irreversible.
