'use strict'

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
            <div class="form-line">
              <label htmlFor="name">Vineyard Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={name}
                onChange={evt => setName(evt.target.value)}
                placeholder="Enter vineyard name"
              />
            </div>
            <div class="form-line">
              <label htmlFor="region">Region:</label>
              <input
                type="text"
                id="region"
                name="region"
                value={region}
                onChange={evt => setRegion(evt.target.value)}
                placeholder="Enter region"
              />
            </div>
            <div class="form-line">
              <label htmlFor="country">Country:</label>
              <input
                type="text"
                id="country"
                name="country"
                value={country}
                onChange={evt => setCountry(evt.target.value)}
                placeholder="Enter country"
              />
            </div>
            <div class="form-line">
              <button type="submit">Save</button>
            </div>
          </form>

      </div>
    </div>
  );
}



function Vineyards() {
  const [vineyards, setVineyards] = React.useState([]);
  const [modalOpen, setModalOpen] = React.useState(false); 
  const [currentVineyard, setCurrentVineyard] = React.useState(null) 
 
  const openModal = (vineyard) => {
    setModalOpen(true);
    setCurrentVineyard(vineyard);
  }

  const closeModal = () => {
    setModalOpen(false);
    setCurrentVineyard(null);
  }


  React.useEffect(() => {
    fetch('/api/get_vineyards')
        .then(res => res.json())
        .then((result) => {
            setVineyards(result)
        });
  }, []);

 
  return (
    <div>
        <ul className="vineyard-list">
            {vineyards.map(vineyard => {
                return(<li className="vineyard-item" key={vineyard.vineyard_id}>
                    {vineyard.name}: {vineyard.region}, {vineyard.country}   
                    <button ClassName="vineyard-edit-button" onClick={() => openModal(vineyard)}>Edit</button>
                </li>)
            })}
        </ul>
        {modalOpen && 
          <VineyardModal 
            vineyard={currentVineyard} 
            closeModal={closeModal} 
            setVineyards={setVineyards}
            vineyards={vineyards}
          />
      }
    </div>
  )
}

ReactDOM.render(<Vineyards />, document.querySelector('#vineyards'));
