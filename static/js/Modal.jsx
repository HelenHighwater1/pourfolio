function Modal({ vineyard, closeModal, setVineyards }) {
  const [name, setName] = React.useState(vineyard.name);
  const [region, setRegion] = React.useState(vineyard.region);
  const [country, setCountry] = React.useState(vineyard.country);

  const handleSubmit = (evt) => {
    evy.preventDefault();
    fetch(`/update_vineyard/${vineyard.vineyard_id}`, {
      method: 'POST',
      body: JSON.stringify({ vineyard_name: name, region, country }),
    })
    .then(response => response.json())
    .then(res => {
        setVineyards(); //FINISH THIS
        closeModal();
    });
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={closeModal}>&times;</span>
        <h1>Edit {vineyard.name}</h1>
        <form onSubmit={handleSubmit}>
          Vineyard name: <input type="text" value={name} onChange={e => setName(e.target.value)} /><br />
          Region: <input type="text" value={region} onChange={e => setRegion(e.target.value)} /><br />
          Country: <input type="text" value={country} onChange={e => setCountry(e.target.value)} /><br />
          <button type="submit">Save</button>
        </form>
      </div>
    </div>
  );
}