title: DuckDuckGo vs Google
summary: Times when DDG has failed me, and I had to resort to Google.

<script>
let modal = document.getElementById("myModal");
let imgs = document.getElementsByTagName("img");
let modalImg = document.getElementById("modalImg");

for (let i = 0; i < imgs.length; i++) {
  imgs[i].addEventListener('click', function(){
​    modal.style.display = "block";
​    modalImg.src = this.src;
​    captionText.innerHTML = this.alt;
  });
}

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
} 
</script>

<style>
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
}

/* Modal Content (Image) */
.modal-content {
  margin: auto;
  display: block;
  max-width: 70rem !important;
  max-height: unset !important;
}

.close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  transition: 0.3s;
}

.close:hover,
.close:focus {
  color: #bbb;
  text-decoration: none;
  cursor: pointer;
}

.wrapper {
  padding-bottom: 100px;
}

img {
  cursor: pointer;
}
img:hover {
  border: 5px solid black;
}

/* 100% Image Width on Smaller Screens */
@media only screen and (max-width: 700px){
  .modal-content {
​    width: 100%;
  }
}

</style>

<!-- Modal -->

<div id="myModal" class="modal">
  <!-- The Close Button -->
  <span class="close">&times;</span>
  <div class="wrapper">
    <img class="modal-content" id="modalImg">
  </div>
  <div id="caption"></div>
</div> 


Sometimes people will talk about how Google results are still better than those provided by DuckDuckGo. This is often why they are hesitant to switch. There's usually not any data to back it up, though, more of a vague feeling that Google has better results. I use DDG on a daily basis, and I'm endeavoring to record the results pages below which force me to use Google to get what I want.


![DDG vs Google search results page](/images/ddg-vs-goog-1.png)

Here's one where I tried to search up "approximate independence", i.e. how to get independent samples, or something close to it.

You can see the DDG results on the left and the Google results on the right. DDG clearly has some irrelevant results, like a unversity page and, oddly enough, a video game listing. On the other hand, Google even provides helpful Math StackExchange, which seems exactly like what I need.



![Another ddg vs google search results page](/images/ddg-vs-goog-2.png)

For this one, I was trying to find a specific paper written by one of my professors. You can see that DDG can't even find the paper, while Google instantly offers up several links.



![yet another ddg vs goog](/images/ddg-vs-goog-3.png)

Once again, I'm trying to find a specific chapter in a statistics book. DDG can't find the paper, while Google has it as the first result.


![yet another ddg vs goog](/images/ddg-vs-goog-4.png)

This time, I'm looking for information about RSS, and I get information about India's current party. Although, to be fair, maybe that does get more hits then the feed protocol.


![yet another ddg vs goog](/images/ddg-vs-goog-5.png)

Great. I'm trying to figure out how to verify whether Signal, the messaging app, has the source code it claims. While DDG does link to Signal, it doesn't have the bit about reproducible builds, which Google has helpfully included.