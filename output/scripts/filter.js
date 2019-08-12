function filterPosts() {
  let n = parseInt(document.querySelector("#num-field").value);
  let posts = document.querySelectorAll(".post-link");
  for (let i = 0; i < posts.length; i++) {
    let c = parseInt(posts[i].dataset.word_count);
    console.log(c);
      if (c <= n) {
        if (this.dataset.toggle === "1") {
          posts[i].style.display = 'none';
        }
        else {
          posts[i].style.display = 'block';
        }
      }
  }
  this.dataset.toggle ^= 1;
  document.querySelector("#num-field").disabled = !document.querySelector("#num-field").disabled;
}
document.querySelector("#checkbox").addEventListener("change", filterPosts);