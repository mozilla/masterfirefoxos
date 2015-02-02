(function(){
  var tinymce_added = {};

  django.jQuery(document).ready(function() {
    tinyMCE.init({
      height: '300',
      paste_auto_cleanup_on_paste: false,
      relative_urls: false,
      invalid_elements: 'script',
      plugins: [
        "code"
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
    contentblock_init_handlers.push(richtext_init_fn);
  });

  var richtext_init_fn = function(){
    $('.order-machine textarea').each(function(){
      add_tinymce(this);
    });
  }

  function add_tinymce(field) {
    var id = field ? field.id : this.id;
    if(!tinymce_added[id]) {
      tinyMCE.execCommand('mceAddEditor', false, id);
      tinymce_added[id] = true;
    }
  }
})();
