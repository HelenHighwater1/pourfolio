function Vineyards() {
  const [vineyards, setVineyards] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/get_vineyards')
        .then(res => res.json())
        .then((result) => {
            console.log(result)
            setVineyards(result)
        });
  }, []);

  return (
    <ul>
        {vineyards.map(vineyard => {
            return(<li>
                {vineyard.name}: {vineyard.region}, {vineyard.country}   
                <form action={`/edit_vineyard/${vineyard.vineyard_id}`}>
                    <button type="submit">Edit</button>
                </form>
            </li>)
        })}
    </ul>
  )
}


ReactDOM.render(<Vineyards />, document.querySelector('#vineyards'));
