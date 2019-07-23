var rb_owner_key = "3a2157b1-a381-11e9-9f0f-040140774501";
var thread_uri = window.location.href;
var thread_title = window.document.title;
var thread_fragment = window.location.hash;

function create_remarkbox_iframe() {
  var src = "https://my.remarkbox.com/embed?rb_owner_key=" + rb_owner_key + "&thread_title=" + thread_title + "&thread_uri=" + thread_uri;
  var ifrm = document.createElement("iframe");
  ifrm.setAttribute("id", "remarkbox-iframe");
  ifrm.setAttribute("scrolling", "no");
  ifrm.setAttribute("src", src);
  ifrm.setAttribute("frameborder", "0");
  ifrm.setAttribute("tabindex", "0");
  ifrm.setAttribute("title", "Remarkbox");
  ifrm.style.width = "100%";
  document.getElementById("remarkbox-div").appendChild(ifrm);
}

document.getElementById("show-comment-button").addEventListener("click", function() {
  create_remarkbox_iframe();
  iFrameResize(
    {
      checkOrigin: ["https://my.remarkbox.com"],
      inPageLinks: true,
      initCallback: function(e) {e.iFrameResizer.moveToAnchor(thread_fragment)}
    },
    document.getElementById("remarkbox-iframe")
  );
  this.style.display = 'none';
});