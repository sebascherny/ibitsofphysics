// Simple Rich Text Editor for Django Admin
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('.rich-text-editor');
    
    textareas.forEach(function(textarea) {
        createRichTextEditor(textarea);
    });
});

function createRichTextEditor(textarea) {
    // Create toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'rich-text-toolbar';
    
    // Add formatting buttons
    const buttons = [
        { name: 'bold', label: 'B', title: 'Bold', tag: 'strong' },
        { name: 'italic', label: 'I', title: 'Italic', tag: 'em' },
        { name: 'underline', label: 'U', title: 'Underline', tag: 'u' },
        { name: 'separator', label: '|' },
        { name: 'h3', label: 'H3', title: 'Heading 3', tag: 'h3' },
        { name: 'p', label: 'P', title: 'Paragraph', tag: 'p' },
        { name: 'separator', label: '|' },
        { name: 'ul', label: '• List', title: 'Bullet List' },
        { name: 'ol', label: '1. List', title: 'Numbered List' },
        { name: 'separator', label: '|' },
        { name: 'link', label: 'Link', title: 'Insert Link' },
        { name: 'separator', label: '|' },
        { name: 'code', label: 'Code', title: 'Code Block', tag: 'code' }
    ];
    
    buttons.forEach(function(btn) {
        if (btn.name === 'separator') {
            const sep = document.createElement('span');
            sep.className = 'toolbar-separator';
            sep.textContent = btn.label;
            toolbar.appendChild(sep);
        } else {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'toolbar-btn';
            button.textContent = btn.label;
            button.title = btn.title;
            button.addEventListener('click', function(e) {
                e.preventDefault();
                handleFormatting(textarea, btn);
            });
            toolbar.appendChild(button);
        }
    });
    
    // Insert toolbar before textarea
    textarea.parentNode.insertBefore(toolbar, textarea);
    
    // Add some helpful text
    const helpText = document.createElement('div');
    helpText.className = 'rich-text-help';
    helpText.innerHTML = '<small>Tip: You can also use HTML tags directly in the text area. Common tags: &lt;strong&gt;, &lt;em&gt;, &lt;h3&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;li&gt;, &lt;a href="..."&gt;</small>';
    textarea.parentNode.insertBefore(helpText, textarea.nextSibling);
}

function handleFormatting(textarea, btn) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    const beforeText = textarea.value.substring(0, start);
    const afterText = textarea.value.substring(end);
    
    let newText = '';
    
    switch(btn.name) {
        case 'bold':
        case 'italic':
        case 'underline':
        case 'code':
        case 'h3':
        case 'p':
            if (selectedText) {
                newText = `<${btn.tag}>${selectedText}</${btn.tag}>`;
            } else {
                newText = `<${btn.tag}></${btn.tag}>`;
            }
            break;
        case 'ul':
            if (selectedText) {
                const lines = selectedText.split('\n').filter(line => line.trim());
                newText = '<ul>\n' + lines.map(line => `  <li>${line.trim()}</li>`).join('\n') + '\n</ul>';
            } else {
                newText = '<ul>\n  <li></li>\n</ul>';
            }
            break;
        case 'ol':
            if (selectedText) {
                const lines = selectedText.split('\n').filter(line => line.trim());
                newText = '<ol>\n' + lines.map(line => `  <li>${line.trim()}</li>`).join('\n') + '\n</ol>';
            } else {
                newText = '<ol>\n  <li></li>\n</ol>';
            }
            break;
        case 'link':
            const url = prompt('Enter URL:');
            if (url) {
                if (selectedText) {
                    newText = `<a href="${url}">${selectedText}</a>`;
                } else {
                    newText = `<a href="${url}">Link Text</a>`;
                }
            } else {
                return;
            }
            break;
    }
    
    textarea.value = beforeText + newText + afterText;
    
    // Set cursor position
    const newCursorPos = start + newText.length;
    textarea.setSelectionRange(newCursorPos, newCursorPos);
    textarea.focus();
}
