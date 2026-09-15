import React, { useState } from 'react';
import './CodeBlock.css';

const CodeBlock = ({ code, language = '', filename = '' }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `code.${language || 'txt'}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Simple syntax highlighting
  const highlightCode = (text, lang) => {
    let highlighted = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Keywords
    highlighted = highlighted.replace(
      /\b(import|export|from|const|let|var|function|class|return|if|else|for|while|async|await|try|catch|new|this|typeof|instanceof)\b/g,
      '<span class="token-keyword">$1</span>'
    );

    // Strings
    highlighted = highlighted.replace(
      /(['"`])(.*?)(['"`])/g,
      '<span class="token-string">$1$2$3</span>'
    );

    // Comments
    highlighted = highlighted.replace(
      /(\/\/.*$|#.*$)/gm,
      '<span class="token-comment">$1</span>'
    );

    // Numbers
    highlighted = highlighted.replace(
      /\b(\d+(?:\.\d+)?)\b/g,
      '<span class="token-number">$1</span>'
    );

    // Functions
    highlighted = highlighted.replace(
      /\b([a-zA-Z_]\w*)(?=\()/g,
      '<span class="token-function">$1</span>'
    );

    return highlighted;
  };

  const displayLang = language || 'text';
  const lines = code.split('\n');

  return (
    <div className="code-block">
      {/* Header */}
      <div className="code-header">
        <div className="code-meta">
          {filename && <span className="code-filename">{filename}</span>}
          <span className="code-lang">{displayLang}</span>
        </div>
        <div className="code-actions">
          <button 
            className={`code-btn ${copied ? 'code-btn--active' : ''}`}
            onClick={handleCopy}
            title="Copy code"
          >
            {copied ? (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>Copied</span>
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>Copy</span>
              </>
            )}
          </button>
          <button 
            className="code-btn"
            onClick={handleDownload}
            title="Download file"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>Download</span>
          </button>
        </div>
      </div>

      {/* Code Content */}
      <div className="code-content">
        <table className="code-table">
          <tbody>
            {lines.map((line, i) => (
              <tr key={i}>
                <td className="code-line-num">{i + 1}</td>
                <td 
                  className="code-line"
                  dangerouslySetInnerHTML={{ __html: highlightCode(line, language) || '&nbsp;' }}
                />
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CodeBlock;
