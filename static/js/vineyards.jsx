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
      <h1>Edit {vineyard.name}</h1>
      <form onSubmit={handleSubmit}>
        Vineyard name: <input type="text" name='name' value={name} onChange={evt => setName(evt.target.value)} /><br />
        Region: <input type="text" name='region' value={region} onChange={evt => setRegion(evt.target.value)} /><br />
        Country: <input type="text" name='country' value={country} onChange={evt => setCountry(evt.target.value)} /><br />
        <button type="submit">Save</button>
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
        <ul>
            {vineyards.map(vineyard => {
                return(<li key={vineyard.vineyard_id}>
                    {vineyard.name}: {vineyard.region}, {vineyard.country}   
                    <button id="editbtn" onClick={() => openModal(vineyard)}>Edit</button>
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
