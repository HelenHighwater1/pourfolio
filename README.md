
<p align="center"><img src="static/imgs/pourfolio-logo.png" width="300" ></p>

# Pourfolio
Pourfolio is wine cellar tracking application. It offers users the ability to create aging schedules, take tasting notes, and review historical tasting data.

A bit of history here - about a year ago, during our honeymoon in France, my husband and I selected some of our favorite wines with the intention of aging them to enjoy on future anniversaries. Initially, we used individual tags to mark the years we planned to drink each bottle... but that ended up being a mess - tags everywhere!

To solve this problem, I developed Pourfolio as a fun, personal project. The app is designed to store aging schedules and tasting notes in one convenient place. This way, whether it’s 10, 20, or even 30 years from now, we can open the exact bottle we intended, and effortlessly add new tasting notes while reviewing those from previous years.

![log-in](static/imgs/login.jpg)

## Features

All site visitors are able to either create their own account, or take a spin on our "Demo User" account to have a look around.  

Key Features:

- User Account Management: Users can create accounts and log in to access their personal wine cellars.
- Cellar Management: Users can view, search, and filter their wine cellars, making it easy to organize and view their collections.
- Wine Addition and Tracking: Users can add new bottles to their cellars, set up aging schedules, and track consumption with detailed tasting notes for each bottle.
- Tasting Note Review: Users can access and review all tasting notes associated with a specific wine, allowing for comparisons and historical tracking.
- Vineyard Management: Users have the capability to create and edit information about vineyards.

![view wine](static/imgs/wine-view.png)

## Technologies

Pourfolio has a backend stack of Python, Flask, Jinja, and SQLAlchemy; using a PostgreSQL database.  Its frontend is Javascript and React, as well as some Bootstrap.  

## Special Features

### React
Although this did not start as a React app, I wanted to test the waters with React.  I kind of sandboxed this by incorporating it into a non-essential part of the app - Vinyards was great because it is a simple table and doesn't really touch anything in the main functionality.  

In the code below, I  use a conditionally rendered modal to edit the vineyard information, save the updates, and then loop through the vineyard list to replace the old vineyard information with the updated information.


```javascript 

function VineyardModal({ vineyard, closeModal, setVineyards, vineyards }) {
  const [name, setName] = React.useState(vineyard.name);
  const [region, setRegion] = React.useState(vineyard.region);
  const [country, setCountry] = React.useState(vineyard.country);

  const handleSubmit = (evt) => {
    evt.preventDefault();

    fetch(`/update_vineyard/${vineyard.vineyard_id}`, {
      method: 'POST',
      body: JSON.stringify({ name, region, country }),
      headers: { 'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(res => {  
        setVineyards(vineyards => vineyards.map(v => v.vineyard_id === vineyard.vineyard_id ? res : v));
        closeModal();
    });
  };
  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={closeModal}>&times;</span>
        <h4>Edit {vineyard.name}</h4>
          <form onSubmit={handleSubmit}>
              ......
          </form>

      </div>
    </div>
  );
}

```

### React Modal 
WILL HAVE GIF OF MODAL IN ACTION

### Ajax

I wanted to use a really dynamic filter function - below you can see that I have one function that will filter the cellar based on both the catagory and the specific value to filter.  This simplifies the backend code into one function, instead of breaking it out to seven functions - one for each value of the filter.    

filters.js:
```javascript 
function apply_filters(evt) {
    evt.preventDefault();
    const filterItm = evt.target.id
    const filterVal = evt.target.value

    const url = `/filter_cellar?filter_on=${filterItm}&filter_val=${filterVal}`

    fetch(url)
        .then(response => response.json())
        .then(res => {    
            document.querySelector('#cellar_lots').innerHTML = '';
            document.querySelector('#filtered-by').innerHTML = `${filterItm}: ${filterVal}`;
         
            res.forEach(lot => {
                document.querySelector('#cellar_lots').insertAdjacentHTML(
                    'beforeend', 
                    `<div class="card" >
                        ......
                    </div>`
                )
            })
            document.querySelector(`#${filterItm}`).value=filterItm
        })
}

```
crud.py: 
```python
def filter_cellar_lots(filter_on, filter_val, cellar_id):
    all_filtered_lots = db.session.query(Lot).filter(
        Lot.cellar_id == cellar_id
        ).where(getattr(Lot, f'{filter_on}') == filter_val).all()
    
    return all_filtered_lots
```


## Coming Soon!!  
- Users can grant other users access to their cellar
- Pourfolio is currently in transiotion to become a full React app.
- "Choose For Me" button - to randomly select an available wine.

# Thanks for visiting!  
Feel free to [get in touch](https://www.heyimhelen.com)!
