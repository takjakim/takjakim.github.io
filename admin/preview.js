(function () {
  const CMS = window.CMS;
  if (!CMS) return;

  CMS.registerPreviewStyle('/styles.css');
  CMS.registerPreviewStyle('/admin/preview.css');

  const h = window.h || (window.React && window.React.createElement);
  if (!h) return;

  const NOTE_COLLECTIONS = ['education', 'ai', 'running', 'dev', 'investing', 'theory'];

  function field(entry, name, fallback = '') {
    const value = entry.getIn(['data', name]);
    return value == null ? fallback : value;
  }

  function listField(entry, name) {
    const value = entry.getIn(['data', name]);
    if (!value) return [];
    if (Array.isArray(value)) return value;
    if (typeof value.toJS === 'function') return value.toJS();
    return [value];
  }

  function formatDate(value) {
    if (!value) return '';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value).slice(0, 10).replace(/-/g, '.');
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${yyyy}.${mm}.${dd}`;
  }

  function tagPills(tags) {
    return h(
      'div',
      { className: 'note-tags', 'aria-label': 'tags' },
      ...tags.map((tag) => h('span', { className: 'tag-pill', key: String(tag) }, `#${tag}`)),
    );
  }

  function NotePreview({ entry, widgetFor }) {
    const title = field(entry, 'title', 'Untitled');
    const date = field(entry, 'last_modified_at') || field(entry, 'date');
    const tags = listField(entry, 'tags');

    return h(
      'article',
      { className: 'note-page decap-note-preview' },
      h(
        'header',
        { className: 'note-header' },
        h('h1', { className: 'note-title' }, title),
        h(
          'div',
          { className: 'note-meta' },
          h('time', { className: 'note-date' }, formatDate(date)),
        ),
        tags.length ? tagPills(tags) : null,
      ),
      h(
        'div',
        { className: 'note-container' },
        h(
          'div',
          { className: 'note-content' },
          widgetFor('body') || h('p', { className: 'decap-preview-empty' }, '본문을 입력하면 여기에 미리보기가 표시됩니다.'),
        ),
      ),
    );
  }

  NOTE_COLLECTIONS.forEach((name) => CMS.registerPreviewTemplate(name, NotePreview));
})();
