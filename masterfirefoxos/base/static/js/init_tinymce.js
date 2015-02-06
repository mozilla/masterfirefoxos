(function(){
  var tinymce_added = {};

  django.jQuery(document).ready(function() {
    tinyMCE.init({
      height: '300',
      paste_auto_cleanup_on_paste: false,
      relative_urls: false,
      invalid_elements: 'script',
      entity_encoding : "raw",
      extended_valid_elements : "-p",
      plugins: [
        "code", "link"
      ],
      toolbar: "undo redo | styleselect | bold italic underline | bullist numlist | link | code",
      statusbar: false,
      menubar : false,
      style_formats: [
        {
          title: "Headers",
          items: [
            {title: "Header 1",format: "h1"},
            {title: "Header 2",format: "h2"},
            {title: "Header 3",format: "h3"},
            {title: "Header 4",format: "h4"},
            {title: "Header 5",format: "h5"},
            {title: "Header 6",format: "h6"}
          ]
        },
        {
          title: "Inline",
          items: [
            {title: "Bold", icon: "bold", format: "bold"},
            {title: "Italic", icon: "italic", format: "italic"},
            {title: "Underline", icon: "underline", format: "underline"},
            {title: "Strikethrough", icon: "strikethrough", format: "strikethrough"},
            {title: "Superscript", icon: "superscript", format: "superscript"},
            {title: "Subscript", icon: "subscript", format: "subscript"},
            {title: "Code", icon: "code", format: "code"}
          ]
        },
        {
          title: "Blocks",
          items: [
            {title: "Paragraph", format: "p"},
            {title: "Blockquote", format: "blockquote"},
            {title: "Div", format: "div"},
            {title: "Pre", format: "pre"}
          ]
        }
      ]
    });
    // contentblock_init_handlers.push(richtext_init_fn);

    django.jQuery('.activate-tinymce').on('click', function(event) {
      event.preventDefault();
      var textfield = django.jQuery(this).siblings()[1]
      tinyMCE.execCommand('mceAddEditor', false, textfield.id);
      django.jQuery(this).remove()
    });
  });
})();
