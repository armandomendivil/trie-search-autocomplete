import { useEffect, useState } from 'react'
import { Layout, Card, Input, Spin } from 'antd'
const { Header, Footer, Content } = Layout
import { Col, Row } from 'antd';
const { Meta } = Card
import './App.css'

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false)
  const [movies, setMovies] = useState([])
  const [debouncedQuery, setDebouncedQuery] = useState('');

  const fetchData = async () => {
    if (!debouncedQuery) return;
    setLoading(true)
    const response = await fetch(`http://localhost:3000/api/search?query=${debouncedQuery}`)
    const json = await response.json()
    setMovies(json.movies)
    setLoading(false)
    console.log(json)
  }

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
    }, 500);

    return () => {
      clearTimeout(handler);
    };
  }, [query]);

  useEffect(() => {
    console.log(debouncedQuery)
    fetchData();
  }, [debouncedQuery])

 
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ color: 'white' }}>SEARCH AUTOCOMPLETE</Header>
      <Content style={{ padding: '24px', background: '#fff' }}>
        <Input onChange={e => setQuery(e.target.value)} placeholder="Search movie ..." style={{ width: '400px', marginBottom: 16 }} />
        {
          !loading && (
            <Row gutter={[16, 16]}>
            {movies.length > 0 && movies.map((movie, i) => (
              <Col span={4} key={i}>
                <Card
                  hoverable
                  style={{ width: 240 }}
                  cover={<img alt="example" src={movie.url} />}
                >
                  <Meta title={movie.word} />
                </Card>
              </Col>
            ))}
          </Row>
          )
        }
        {
          loading && (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
              <Spin />
            </div>
          )
        }
      </Content>
      <Footer>footer</Footer>
    </Layout>
  )
}

export default App
