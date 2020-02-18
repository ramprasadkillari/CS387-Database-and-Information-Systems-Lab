import React, { useState } from "react";
import ReactDOM from "react-dom";
import data from "./data.json";
import "./styles.css";

const elements = data.elements;
// const tot = elements.length;
// function Counter(props) {
//   return <button> Counter: {props.name} </button>;
// }

function PeriodicTable(props) {
  const categories = [
    "alkali metal",
    "alkaline earth metal",
    "lanthanide",
    "actinide",
    "transition metal",
    "post-transition metal",
    "metalloid",
    "noble gas",
    "diatomic nonmetal",
    "polyatomic nonmetal",
    "unknown, probably transition metal",
    "unknown, probably post-transition metal",
    "unknown, probably metalloid",
    "unknown, predicted to be noble gas",
    "unknown, but predicted to be an alkali metal"
  ];
  const [states, setStates] = useState({
    "alkali metal": true,
    "alkaline earth metal": true,
    lanthanide: true,
    actinide: true,
    "transition metal": true,
    "post-transition metal": true,
    metalloid: true,
    "noble gas": true,
    "diatomic nonmetal": true,
    "polyatomic nonmetal": true,
    "unknown, probably transition metal": true,
    "unknown, probably post-transition metal": true,
    "unknown, probably metalloid": true,
    "unknown, predicted to be noble gas": true,
    "unknown, but predicted to be an alkali metal": true
  });

  var check_boxes = [];
  categories.map(categ =>
    check_boxes.push(
      <div>
        <label>
          {" "}
          <input
            type="checkbox"
            className={categ}
            defaultChecked
            onChange={check_handler}
          />{" "}
          {categ}
          <br />{" "}
        </label>
      </div>
    )
  );

  function check_handler(event) {
    var newst = { ...states };
    newst[event.target.className] = !states[event.target.className];
    setStates(newst);
  }

  return (
    <div>
      <div className="wrapper">
        {elements.map((element, i) => {
          var divstyle = {
            gridColumn: element.xpos,
            gridRow: element.ypos
          };
          return (
            <div style={divstyle}>
              {(function() {
                if (states[element.category]) {
                  return (
                    <Cell
                      name={element.symbol}
                      atnum={element.number}
                      category={element.category}
                    />
                  );
                }
              })()}
            </div>
          );
        })}
      </div>
      {check_boxes}
    </div>
  );
}

function Cell(props) {
  var colour = "#ff6666";
  if (props.category === "alkali metal") colour = "#ff6666";
  else if (props.category === "alkaline earth metal") colour = "#fedead";
  else if (props.category === "lanthanide") colour = "#ffbffe";
  else if (props.category === "actinide") colour = "#ff99cb";
  else if (props.category === "transition metal") colour = "#ffc0bf";
  else if (props.category === "post-transition metal") colour = "#cccccc";
  else if (props.category === "metalloid") colour = "#cccc9a";
  else if (props.category === "noble gas") colour = "#c1feff";
  else if (props.category === "diatomic nonmetal") colour = "#f1ff90";
  else if (props.category === "polyatomic nonmetal") colour = "#f1ff90";
  else if (props.category === "unknown, probably transition metal")
    colour = "#e8e8e8";
  else if (props.category === "unknown, probably post-transition metal")
    colour = "#e8e8e8";
  else if (props.category === "unknown, probably metalloid") colour = "#e8e8e8";
  else if (props.category === "unknown, predicted to be noble gas")
    colour = "#e8e8e8";
  else if (props.category === "unknown, but predicted to be an alkali metal")
    colour = "#e8e8e8";
  else colour = "#e8e8e8";

  return (
    <div className="cell" style={{ background: colour }}>
      <div>
        <p> {props.atnum}</p>
        <p>{props.name} </p>
      </div>
    </div>
  );
}

const cellElement = document.getElementById("cell"); //see index.html
ReactDOM.render(<PeriodicTable />, cellElement);
