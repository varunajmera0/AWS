import React, { useState, useEffect } from "react";
import {
  Grid,
  Image,
  Segment,
  Button,
  Header,
  Form,
  Card,
  Loader,
} from "semantic-ui-react";
import "semantic-ui-css/semantic.min.css";
import { GraphLine } from "./Line";
import axios from "axios";

const App = () => {
  const [stock, setStock] = useState("");
  const [stockinfo, setStockinfo] = useState("");
  const [loaderstockinfo, setLoaderstockinfo] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    console.log("Triggered!", offset);
    if (loading) {
      const sse = new EventSource(
        `http://127.0.0.1:5002/consume/${stock}/${offset}`
      );
      function handleStream(e) {
        console.log("E", e);
        const data = JSON.parse(e.data);

        setData((prevState) => [
          ...prevState,
          {
            datetime: data["Datetime"],
            closedrop: data["Close_drop"],
            symbol: data["symbol"],
          },
        ]);
        setOffset(data["offset"]);
      }
      sse.onmessage = (e) => handleStream(e);
      sse.onerror = (e) => sse.close();

      return () => sse.close();
    }
  }, [loading]);

  useEffect(() => {
    if (stock === "") {
      setLoaderstockinfo("");
    }
  }, [stock]);

  const sendPing = () => {
    setLoading(false);
    setLoaderstockinfo(true);

    fetch(
      "<AWS API_Gateway_url>/createSymbol", //https://3bdt3by8wi.execute-api.us-east-1.amazonaws.com/
      {
        mode: "cors",
        method: "POST",
        body: JSON.stringify({ symbol: stock }),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        setStockinfo(data.Item);
        setLoaderstockinfo(false);
      });

    axios.post("http://127.0.0.1:5000", { symbol: stock }).then((response) => {
      console.log("res", response);
      setLoading(true);
      setOldstock(stock);
      setData([]);
    });
  };

  const CardInfo = () => {
    if (stockinfo !== "") {
      return (
        <Card>
          <Card.Content>
            <Image floated="right" size="mini" src={stockinfo["logo_url"]} />
            <Card.Header>
              {stockinfo["longName"] || stockinfo["symbol"]}
            </Card.Header>
            <Card.Meta>{stockinfo["industry"]}</Card.Meta>
            <Card.Description>
              Market: {stockinfo["market"]} <br />
              Exchange: {stockinfo["exchange"]}
            </Card.Description>
          </Card.Content>
          <Card.Content extra>
            <div className="ui two buttons">
              <Button basic color="green">
                {stockinfo["city"]}, {stockinfo["state"]},{" "}
                {stockinfo["country"]}
              </Button>
            </div>
          </Card.Content>
        </Card>
      );
    } else {
      return (
        <Loader active={loaderstockinfo}>Loading Stock Information</Loader>
      );
    }
  };

  return (
    <Grid.Row>
      <Grid centered columns={4}>
        <Grid.Column>
          <Header as="h2" textAlign="center">
            Stock
          </Header>
          <Segment>
            <Form size="large">
              <Form.Input
                fluid
                icon="briefcase"
                iconPosition="left"
                onChange={(e) => setStock(e.target.value)}
                placeholder="Search Stock..."
              />

              <Button
                color="blue"
                fluid
                size="large"
                onClick={() => sendPing()}
                disabled={loaderstockinfo && loading}
              >
                Search
              </Button>
            </Form>
          </Segment>
        </Grid.Column>
        <Grid.Column>
          <CardInfo />
        </Grid.Column>
      </Grid>

      <Grid centered columns={2}>
        <Grid.Column>
          <Header as="h2" textAlign="center">
            {stock.toUpperCase()} Stock
          </Header>
        </Grid.Column>
      </Grid>

      <Grid centered columns={2}>
        <Grid.Column>
          {loading ? (
            <GraphLine data={data} />
          ) : (
            <Loader active={!loading}>
              Loading historical data for {stock || "stock"}
            </Loader>
          )}
        </Grid.Column>
      </Grid>
    </Grid.Row>
  );
};

export default App;
