import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Head';
import Search from './components/Search';

const handleSearchSubmit = (e) => {
  console.log(e);
}

function App() {
  return (
    <div>
      <Header title="Images Gallery"/>
      <Search handleSubmit={handleSearchSubmit}/>
    </div>
  );
}

export default App;
