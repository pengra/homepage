// Grab the results as the user types
const onInputUpdate = (box, event) => {
  // On Input Update
  grabResults(box, event)
  updateSearchSettings(box)
}

const updateSearchSettings = (box) => {
  const value = box.value
  if (value.length === 0 || value.slice(0, 1) === '/') {
    document.getElementById("search_details").style.display = "none"
  } else {
    document.getElementById("search_details").style.display = "block"
    document.getElementById("search_copy").innerText = value
  }
}

const grabResults = (box, event) => {
  const value = box.value
  const is_news = document.getElementById('is_news').checked
  const force = event.keyCode === 13 ? '&force=1' : ''
  const is_academic = document.getElementById('is_academic').checked ? '&academic=1' : ''
  const is_scholarly = document.getElementById('is_scholarly').checked ? '&scholarly=1' : ''
  
  if (value === '/hackernews') {
    clearResults()
    clearNews()
    showThinking()
    fetch('/search/?hackernews=1' + force)
      .then((e) => e.json())
      .then((e) => {
        clearResults()
        if (e.results.length > 0) {
          e.results.map((e) => {
            addResult(e.id, e.title, e, e.url, e.blurb)
          })
        }
      })
  } else if (value.slice(0,3) === '/wg') {
    clearResults()
    clearNews()
    showThinking()
    fetch('/search/?wg=1' + force)
      .then((e) => e.json())
      .then((e) => {
        clearResults()
        if (e.results.length > 0) {
          e.results.map((e) => {
            addResult(e.id, e.title, e, e.url, e.blurb)
          })
        }
      })
  } else if (value.slice(0,6) === '/admin') {
    location.href = '/admin/'
  } else if (value.slice(0, 4) === '/api') {
    const query = value.slice(5)
    clearResults()
    clearNews()
    addResult(-1, "API Query Access", {personal: true}, "/search/?query=" + encodeURIComponent(query) + force, "Click to visit the API page for results.")
    addResult(-1, "Admin Page", {personal: true}, "/admin/", "The admin page.")
  } else if (value.slice(0, 5) === '/news' || is_news) {
    const query = value.slice(0, 5) === '/news' ? value.slice(6) : value
    if (query) {
      if (force) {
        showThinking()
      }
      fetch('/search/?news=1&query=' + encodeURIComponent(query) + force)
        .then((e) => e.json())
        .then((e) => {
          clearResults()
          clearNews()
          if (e.results.length > 0) {
            e.results.map((e) => {
              addResult(e.id, e.title, e, e.url, e.blurb)
            })
          } else {
            encourageEnter()
          }
        })
    }
  } else if (value.slice(0, 1) === '/') {
    showCommands()
  } else if (value.length > 0) {
    if (value.includes('java') || value.includes('C++') || value.includes('django') || value.includes('python')) {
      document.getElementById('is_programming').checked = true
    }
    if (force) {
      showThinking()
    }
    fetch('/search/?query=' + value + force + is_academic + is_scholarly)
      .then((e) => e.json())
      .then((e) => {
        clearResults()
        clearNews()
        let stories = 3
        if (e.results.length > 0) {
          e.results.map((e) => {
            if (e.news && stories > 0) {
              addStory(e.id, e.title, e, e.url, e.blurb)
              stories -= 1
            } else {
              addResult(e.id, e.title, e, e.url, e.blurb)
            }
          })
          if (stories === 3) {
            encourageNewsUpdate()
          }
        } else if (!force) {
          encourageEnter()
        }
      })
  } else if (event.keyCode === 8) {
    clearResults()
    clearNews()
  }
}

// Clear all news cards on page
const clearNews = () => {
  document.getElementById('news').innerHTML = ""
}

const showCommands = () => {
  clearNews()
  clearResults()
  addResult(-1, "Commands", {personal: true}, "", "Commands available")
  addResult(-1, "/hackernews", {personal: true}, "", "Show the hottest items on hackernews within the last hour.")
  addResult(-1, "/api <query>", {personal: true}, "", "Get the API link to a search query")
  addResult(-1, "/admin", {personal: true}, "", "Go to the admin page.")
  addResult(-1, "/news <query>", {personal: true}, "", "Show the latest news regarding this query")
  addResult(-1, "/wg", {personal: true}, "", "Show the front page of /wg/")
}

// Add a story card
const addStory = (id, title, badges, url, blurb) => {
  const story = document.createElement("div")
  story.setAttribute("class", "col-md-4")

  const card = document.createElement("div")
  card.setAttribute("class", "card")

  const cardBody = document.createElement("div")
  cardBody.setAttribute("class", "card-body")

  const cardTitle = document.createElement("h5")
  cardTitle.setAttribute("class", "card-title")
  cardTitle.appendChild(document.createTextNode(title))

  const cardText = document.createElement("p")
  cardText.setAttribute("class", "card-text")
  cardText.appendChild(document.createTextNode(blurb))

  const cardLink = document.createElement("a")
  cardLink.setAttribute("href", "/go/" + id + "/")
  cardLink.setAttribute("class", "card-link")
  cardLink.appendChild(document.createTextNode("Read Article"))
  
  cardBody.appendChild(cardTitle)
  cardBody.appendChild(cardText)
  if (url) {
    cardBody.appendChild(cardLink)
  }
  card.appendChild(cardBody)
  story.appendChild(card)
  document.getElementById('news').appendChild(story)
}

// Encourage user to hit enter for news update
const encourageNewsUpdate = () => {
  clearNews()
  addStory(-1, "No Auto Stories", [], "", "Try prepending \"/news\" to your query")
}

// Clear all results on page
const clearResults = () => {
  document.getElementById('results').innerHTML = ""
}

// Show that the page is loading results
const showThinking = () => {
  clearResults()
  addResult(-1, "Thinking...", {personal: true}, "", "Fetching Results")
}

// When there are no search results
const encourageEnter = () => {
  clearResults()
  addResult(-1, "Hit Enter to Search", {personal: true}, "", "No Auto Results")
}

// Add a result to the page
const addResult = (id, title, tags, url, preview) => {
  // <div class="row"></div>
  const result = document.createElement('div')
  result.setAttribute('class', 'row')

  if (tags.personal) {
    result.style.borderLeft = "3px solid #bada55"
  } else if (tags.arxiv) {
    result.style.borderLeft = "3px solid #B31B1B"
  } else if (tags.wiki) {
    result.style.borderLeft = '3px solid #333'
  } else if (tags.hackernews) {
    result.style.borderLeft = "3px solid #ff6600"
  } else if (tags.uw) {
    result.style.borderLeft = "3px solid #4b2e83"
  } else if (tags.chan) {
    result.style.borderLeft = "3px solid #800000"
  }

  // <div class="col-md-10"></div>
  const leftSide = document.createElement('div')
  const rightSide = document.createElement('div')
  if (tags.image) {
    leftSide.setAttribute('class', 'col-md-8')
    rightSide.setAttribute('class', 'col-md-4')
  } else {
    leftSide.setAttribute('class', 'col-md-12')
    rightSide.style.display = 'none'
  }
  

  // <h5>title</h5>
  const resultTitle = document.createElement('h5')
  resultTitle.appendChild(document.createTextNode(title))

  // tags

  // <a href="url">url</a>
  const link = document.createElement('a')
  if (id === -1) {
    link.setAttribute('href', url)
  } else {
    link.setAttribute('href', "/go/" + id + "/")
  }
  link.setAttribute('target', '_blank')
  link.appendChild(document.createTextNode(url))

  const linkMenu = document.createElement('span')
  linkMenu.setAttribute('class', 'dropdown show')

  const dropdownArrow = document.createElement('a')
  dropdownArrow.setAttribute('class', 'dropdown-toggle')
  dropdownArrow.setAttribute('href', '#')
  dropdownArrow.setAttribute('data-toggle', 'dropdown')
  dropdownArrow.setAttribute('aria-haspopup', 'true')
  dropdownArrow.setAttribute('aria-expanded', 'false')

  const dropdownMenu = document.createElement('div')
  dropdownMenu.setAttribute('class', 'dropdown-menu')

  // redirect to: '/admin/search/result/{id}/change/'
  const editButton = document.createElement('div')
  const editLink = document.createElement('a')
  editButton.setAttribute('class', 'dropdown-item')
  editLink.setAttribute('href', '/admin/search/result/' + id + '/change/')
  editLink.setAttribute('target', '_blank')
  editLink.appendChild(document.createTextNode('Edit'))
  editButton.appendChild(editLink)
  
  const removeButton = document.createElement('div')
  removeButton.setAttribute('class', 'dropdown-item')
  const removeLink = document.createElement('a')
  editButton.setAttribute('class', 'dropdown-item')
  removeLink.setAttribute('href', '/admin/search/result/' + id + '/delete/')
  removeLink.setAttribute('target', '_blank')
  removeLink.appendChild(document.createTextNode('Remove'))
  removeButton.appendChild(removeLink)

  const idStat = document.createElement('div')
  idStat.setAttribute('class', 'dropdown-item disabled')
  idStat.appendChild(document.createTextNode('id: ' + id))

  dropdownMenu.appendChild(editButton)
  dropdownMenu.appendChild(removeButton)
  dropdownMenu.appendChild(idStat)
  linkMenu.appendChild(dropdownArrow)
  linkMenu.appendChild(dropdownMenu)

  // <p>blurb</p>
  const blurb = document.createElement('p')
  blurb.appendChild(document.createTextNode(preview))
  // blurb.innerHTML = preview

  leftSide.appendChild(resultTitle)
  leftSide.appendChild(link)
  if (url) {
    leftSide.appendChild(document.createTextNode(" "))
    leftSide.appendChild(linkMenu)
  }
  leftSide.appendChild(blurb)
  if (tags.image) {
    const image = document.createElement('img')
    image.src = tags.image
    image.setAttribute('class', 'img-thumbnail')
    rightSide.appendChild(image)
  }
  result.appendChild(leftSide)
  result.appendChild(rightSide)
  document.getElementById('results').appendChild(result)
}