# Warmgold Frontend — Reference

Extended component implementations and patterns. See SKILL.md for core tokens and philosophy.

## Button Variants

```html
<!-- Primary -->
<button class="btn btn-primary">Save</button>

<!-- Secondary -->
<button class="btn btn-secondary">Cancel</button>

<!-- Danger (reveals on hover) -->
<button class="btn btn-danger">Delete</button>

<!-- Icon button -->
<button class="btn btn-icon" aria-label="Close">
    <svg>...</svg>
</button>

<!-- Loading state -->
<button class="btn btn-primary loading" disabled>
    <span class="spinner"></span>
    Saving...
</button>
```

```css
.btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
    min-height: 44px;
}

.btn-primary {
    background: var(--color-accent);
    color: white;
}
.btn-primary:hover { filter: brightness(1.08); }
.btn-primary:active { filter: brightness(0.95); }

.btn-secondary {
    background: var(--color-bg-card);
    color: var(--color-text-body);
    border: 1px solid var(--color-border);
}
.btn-secondary:hover {
    background: var(--color-bg-sidebar);
    border-color: var(--color-text-muted);
}

.btn-danger {
    background: #e5e5e5;
    color: #737373;
}
.btn-danger:hover {
    background: var(--color-error-bg);
    color: var(--color-error);
}

.btn-icon {
    padding: var(--space-2);
    background: transparent;
    border-radius: var(--radius-sm);
    min-width: 44px;
    min-height: 44px;
    justify-content: center;
}
.btn-icon:hover { background: var(--color-bg-sidebar); }

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}
```

## Card Variants

```html
<!-- Standard Card -->
<article class="card">
    <div class="card-header">
        <h3 class="card-title">Title</h3>
        <span class="badge">Status</span>
    </div>
    <div class="card-body">
        <p>Content here.</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-secondary">Cancel</button>
        <button class="btn btn-primary">Confirm</button>
    </div>
</article>

<!-- Hero Card -->
<article class="card card-hero">
    <div class="card-body">
        <h2>Welcome</h2>
        <p>Key information.</p>
    </div>
</article>
```

```css
.card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

.card-hero {
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-lg);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-5) var(--space-6);
    border-bottom: 1px solid var(--color-border-light);
}

.card-title {
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--color-text-heading);
    margin: 0;
}

.card-body {
    padding: var(--space-6);
}

.card-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-3);
    padding: var(--space-4) var(--space-6);
    border-top: 1px solid var(--color-border-light);
}
```

## Form Elements

```html
<div class="form-group">
    <label class="form-label" for="name">Name</label>
    <input class="form-input" type="text" id="name" placeholder="Enter name">
    <p class="form-hint">Required. Max 100 characters.</p>
</div>

<div class="form-group form-error">
    <label class="form-label" for="email">Email</label>
    <input class="form-input" type="email" id="email" aria-describedby="email-error">
    <p class="form-error-text" id="email-error">Please enter a valid email.</p>
</div>

<div class="form-group">
    <label class="form-label" for="type">Type</label>
    <select class="form-input" id="type">
        <option value="">Select...</option>
        <option>Option A</option>
    </select>
</div>
```

```css
.form-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
    margin-bottom: var(--space-5);
}

.form-label {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-heading);
}

.form-input {
    padding: 10px var(--space-3);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    color: var(--color-text-heading);
    background: var(--color-bg-card);
    transition: border-color var(--transition-fast);
    min-height: 44px;
}

.form-input:focus {
    outline: none;
    border-color: var(--color-text-muted);
    box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-input::placeholder {
    color: var(--color-text-muted);
}

.form-hint {
    font-size: var(--font-size-xs);
    color: var(--color-text-muted);
    margin: 0;
}

.form-error .form-input {
    border-color: var(--color-error);
}

.form-error-text {
    font-size: var(--font-size-xs);
    color: var(--color-error);
    margin: 0;
}
```

## Navigation

```html
<nav class="sidebar-nav" aria-label="Main">
    <a href="#dashboard" class="nav-item active">
        <svg class="nav-icon">...</svg>
        Dashboard
    </a>
    <a href="#cases" class="nav-item">
        <svg class="nav-icon">...</svg>
        Cases
        <span class="badge badge-count">12</span>
    </a>
    <a href="#settings" class="nav-item">
        <svg class="nav-icon">...</svg>
        Settings
    </a>
</nav>
```

```css
.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.nav-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    color: var(--color-text-body);
    text-decoration: none;
    font-size: var(--font-size-sm);
    transition: all var(--transition-fast);
    position: relative;
}

.nav-item:hover {
    background: var(--color-bg-card);
    color: var(--color-text-heading);
}

.nav-item.active {
    background: var(--color-bg-card);
    color: var(--color-text-heading);
    font-weight: 500;
    box-shadow: var(--shadow-sm);
    border-left: 3px solid var(--color-accent);
    padding-left: calc(var(--space-4) - 3px);
}

.nav-icon {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
}
```

## Badge / Pill

```css
.badge {
    display: inline-flex;
    align-items: center;
    padding: 2px var(--space-3);
    border-radius: var(--radius-pill);
    font-size: var(--font-size-xs);
    font-weight: 500;
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.badge-success { background: var(--color-success-bg); color: var(--color-success); }
.badge-error { background: var(--color-error-bg); color: var(--color-error); }
.badge-warning { background: var(--color-warning-bg); color: var(--color-warning); }
.badge-count { background: var(--color-bg-sidebar); color: var(--color-text-muted); }
```

## Toast Notifications

```javascript
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container')
        ?? createToastContainer();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <span class="toast-icon">${type === 'success' ? '&#10003;' : '&#10007;'}</span>
        <span>${escapeHtml(message)}</span>
    `;

    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('toast-visible'));

    setTimeout(() => {
        toast.classList.remove('toast-visible');
        toast.addEventListener('transitionend', () => toast.remove());
    }, 4000);

    // Announce to screen readers
    document.getElementById('status-announcer').textContent = message;
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
    return container;
}
```

```css
#toast-container {
    position: fixed;
    bottom: var(--space-6);
    right: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    z-index: 1000;
}

.toast {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-5);
    border-radius: var(--radius-md);
    font-size: var(--font-size-sm);
    box-shadow: var(--shadow-md);
    opacity: 0;
    transform: translateY(10px);
    transition: all var(--transition-normal);
}

.toast-visible {
    opacity: 1;
    transform: translateY(0);
}

.toast-success {
    background: var(--color-bg-sidebar);
    color: var(--color-text-heading);
}
.toast-success .toast-icon { color: var(--color-success); }

.toast-error {
    background: var(--color-error-bg);
    color: #991B1B;
}
.toast-error .toast-icon { color: var(--color-error); }
```

## Modal / Dialog

```html
<dialog class="modal" id="confirm-modal">
    <div class="modal-content">
        <header class="modal-header">
            <h2 class="modal-title">Confirm Action</h2>
            <button class="btn btn-icon modal-close" aria-label="Close">
                <svg>...</svg>
            </button>
        </header>
        <div class="modal-body">
            <p>Are you sure?</p>
        </div>
        <footer class="modal-footer">
            <button class="btn btn-secondary" data-action="cancel">Cancel</button>
            <button class="btn btn-primary" data-action="confirm">Confirm</button>
        </footer>
    </div>
</dialog>
```

```css
.modal {
    border: none;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    padding: 0;
    max-width: 480px;
    width: 90vw;
}

.modal::backdrop {
    background: rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-5) var(--space-6);
    border-bottom: 1px solid var(--color-border-light);
}

.modal-title {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--color-text-heading);
    margin: 0;
}

.modal-body { padding: var(--space-6); }

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-3);
    padding: var(--space-4) var(--space-6);
    border-top: 1px solid var(--color-border-light);
}
```

```javascript
// Open
document.getElementById('confirm-modal').showModal();

// Close on backdrop click
modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.close();
});

// Close on cancel/confirm
modal.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        modal.close(action);
    });
});
```

## Table

```css
.table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--font-size-sm);
}

.table th {
    text-align: left;
    padding: var(--space-3) var(--space-4);
    font-weight: 500;
    color: var(--color-text-muted);
    font-size: var(--font-size-xs);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--color-border);
}

.table td {
    padding: var(--space-3) var(--space-4);
    color: var(--color-text-body);
    border-bottom: 1px solid var(--color-border-light);
}

.table tr:hover td {
    background: var(--color-bg-sidebar);
}
```

## Loading States

```css
.spinner {
    width: 16px;
    height: 16px;
    border: 2px solid var(--color-border);
    border-top-color: var(--color-accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Skeleton loading */
.skeleton {
    background: linear-gradient(
        90deg,
        var(--color-bg-sidebar) 25%,
        var(--color-border-light) 50%,
        var(--color-bg-sidebar) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: var(--radius-sm);
}

@keyframes shimmer { to { background-position: -200% 0; } }

.skeleton-text { height: 14px; margin-bottom: var(--space-2); }
.skeleton-heading { height: 24px; width: 60%; margin-bottom: var(--space-4); }
```

## Segmented Control (iOS-style)

```html
<div class="segmented-control" role="radiogroup" aria-label="View">
    <button role="radio" aria-checked="true" class="segment active">List</button>
    <button role="radio" aria-checked="false" class="segment">Grid</button>
    <button role="radio" aria-checked="false" class="segment">Map</button>
</div>
```

```css
.segmented-control {
    display: inline-flex;
    background: var(--color-bg-sidebar);
    border-radius: var(--radius-pill);
    padding: 3px;
    gap: 2px;
}

.segment {
    padding: var(--space-2) var(--space-5);
    border: none;
    border-radius: var(--radius-pill);
    background: transparent;
    font-family: var(--font-family);
    font-size: var(--font-size-sm);
    color: var(--color-text-muted);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.segment.active {
    background: var(--color-bg-card);
    color: var(--color-text-heading);
    font-weight: 500;
    box-shadow: var(--shadow-sm);
}
```

## Empty States

```html
<div class="empty-state">
    <svg class="empty-icon">...</svg>
    <h3>No cases yet</h3>
    <p>Upload your first case to get started.</p>
    <button class="btn btn-primary">Upload Case</button>
</div>
```

```css
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-12) var(--space-6);
    text-align: center;
    color: var(--color-text-muted);
}

.empty-state h3 {
    color: var(--color-text-heading);
    margin: var(--space-4) 0 var(--space-2);
}

.empty-state p {
    margin: 0 0 var(--space-6);
    max-width: 320px;
}

.empty-icon {
    width: 48px;
    height: 48px;
    color: var(--color-border);
}
```
