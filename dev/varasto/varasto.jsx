import React from "react";

const tuotteet = [
  {"id":1,"nimi":"Valkoiset muovipöydät","maara":250,"kategoria":"Pöydät","naytto":true},
  {"id":2,"nimi":"Ikeapöydät","maara":28,"kategoria":"Pöydät","naytto":true},
  {"id":3,"nimi":"Vaneripöydät B","maara":57,"kategoria":"Pöydät","naytto":true},
  {"id":4,"nimi":"Vaneripöydät C","maara":78,"kategoria":"Pöydät","naytto":true},
  {"id":5,"nimi":"Vaneripöydät D","maara":18,"kategoria":"Pöydät","naytto":true},
  {"id":6,"nimi":"Vaneripöydät E","maara":100,"kategoria":"Pöydät","naytto":true},
  {"id":7,"nimi":"Vaneripöydät G","maara":158,"kategoria":"Pöydät","naytto":true},
  {"id":8,"nimi":"Vaneripöydät H","maara":16,"kategoria":"Pöydät","naytto":true},
  {"id":9,"nimi":"Vaneripöydät F-info","maara":3,"kategoria":"Pöydät","naytto":true},
  {"id":10,"nimi":"Tuoli","maara":1300,"kategoria":"Tuolit","naytto":true},
  {"id":11,"nimi":"Sohva","maara":4,"kategoria":"Tuolit","naytto":true},
  {"id":12,"nimi":"Säkkituoli, musta","maara":4,"kategoria":"Tuolit","naytto":true},
  {"id":13,"nimi":"Tehokone","maara":20,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":14,"nimi":"Pelikone","maara":20,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":15,"nimi":"Yleisnäyttö","maara":40,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":16,"nimi":"Pelinäyttö","maara":40,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":17,"nimi":"Medialäppäri","maara":30,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":18,"nimi":"PROVO Matto - Hiirimatto","maara":35,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":19,"nimi":"PROVO KUMU PRO - 7.1 tilaäänipelikuuloke","maara":30,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":20,"nimi":"PROVO NOSTE PRO - hiiri","maara":30,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":21,"nimi":"PROVO KAJO OPTO - Näppäimistö","maara":30,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":22,"nimi":"Esperanza EG102","maara":10,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":23,"nimi":"Toimisto näppäimistö","maara":50,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":24,"nimi":"Toimistohiiri","maara":50,"kategoria":"Koneet ja toimistotarvikkeet","naytto":true},
  {"id":25,"nimi":"Toimistotuolit","maara":40,"kategoria":"Tuolit","naytto":true},
  {"id":26,"nimi":"info-tv","maara":87,"kategoria":"TV","naytto":true},
  {"id":27,"nimi":"Kuluttaja-tv","maara":17,"kategoria":"TV","naytto":true},
  {"id":28,"nimi":"TV virtakaapeli ja hdmi kaapeli","maara":100,"kategoria":"TV","naytto":true},
  {"id":29,"nimi":"Tv lattiajalat","maara":29,"kategoria":"TV","naytto":true},
  {"id":30,"nimi":"TV Trussi-kiinnitys","maara":20,"kategoria":"TV","naytto":true},
  {"id":31,"nimi":"Tv pöytäjalat","maara":28,"kategoria":"TV","naytto":true},
  {"id":32,"nimi":"Sähköt 230V","maara":21,"kategoria":"Sähkö","naytto":true},
  {"id":33,"nimi":"Sähköt 1x16A 230V 3000W","maara":21,"kategoria":"Sähkö","naytto":true},
  {"id":34,"nimi":"Sähköt 3x16A 400V 9000W","maara":20,"kategoria":"Sähkö","naytto":true},
  {"id":35,"nimi":"Sähköt 3x32A 400V 15000W","maara":20,"kategoria":"Sähkö","naytto":true},
  {"id":36,"nimi":"Sähköt Muu","maara":10,"kategoria":"Sähkö","naytto":true},
  {"id":37,"nimi":"verkko-1G Base-T","maara":1000,"kategoria":"Verkko","naytto":true},
  {"id":38,"nimi":"verkko-10G SR","maara":1000,"kategoria":"Verkko","naytto":true},
  {"id":39,"nimi":"verkko-10G LR","maara":1000,"kategoria":"Verkko","naytto":true},
  {"id":40,"nimi":"Verkkokaapeli","maara":1000,"kategoria":"Verkko","naytto":true},
  {"id":41,"nimi":"Standi paketti Custom","maara":4,"kategoria":"Standipaketit ja loossit","naytto":true},
  {"id":42,"nimi":"Ständialueen matotus per neliömetri","maara":10000,"kategoria":"Standipaketit ja loossit","naytto":true},
  {"id":43,"nimi":"Standipaketti 4x4m","maara":10,"kategoria":"Standipaketit ja loossit","naytto":true},
  {"id":44,"nimi":"Standipaketti 6x4m","maara":10,"kategoria":"Standipaketit ja loossit","naytto":true},
  {"id":45,"nimi":"Standipaketti 6x8m","maara":10,"kategoria":"Standipaketit ja loossit","naytto":true},
  {"id":46,"nimi":"Spottivalot","maara":10,"kategoria":"Valot","naytto":true},
  {"id":47,"nimi":"Valaistus","maara":1000,"kategoria":"Valot","naytto":true},
  {"id":48,"nimi":"Lasiovinen jääkaappi","maara":2,"kategoria":"Kodinkoneet","naytto":true},
  {"id":49,"nimi":"Lasi-ikkunallinen arkkupakastin","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":50,"nimi":"Pullonkeräys tynnyrit","maara":30,"kategoria":"Kodinkoneet","naytto":true},
  {"id":51,"nimi":"Arkkupakastin","maara":2,"kategoria":"Kodinkoneet","naytto":true},
  {"id":52,"nimi":"Jenkkikaappi","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":53,"nimi":"Jääkaappipakastin","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":54,"nimi":"Kiertoilmauuni","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":55,"nimi":"Kylmälaari","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":56,"nimi":"Metallinen jääkaappi/pakastin","maara":1,"kategoria":"Kodinkoneet","naytto":true},
  {"id":57,"nimi":"Mikro","maara":2,"kategoria":"Kodinkoneet","naytto":true},
  {"id":58,"nimi":"Induktioliesi","maara":5,"kategoria":"Kodinkoneet","naytto":true},
  {"id":59,"nimi":"Taittojalka","maara":2,"kategoria":"Muut","naytto":true},
  {"id":60,"nimi":"Valkokangas","maara":1,"kategoria":"Muut","naytto":true},
  {"id":61,"nimi":"RGB lediputki 201cm pyöreä","maara":188,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":62,"nimi":"RGB lediputki 201cm litteä","maara":26,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":63,"nimi":"360 led-360 led-yksipäinen-50","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":64,"nimi":"360 led-360 led-kaksipäinen-250","maara":26,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":65,"nimi":"360 led-360 led-kaksipäinen-150","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":66,"nimi":"360 led-360 led-kaksipäinen-100","maara":43,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":67,"nimi":"360 led-360 led-kaksipäinen-50","maara":39,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":68,"nimi":"360 led-360 led-yksipäinen-250","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":69,"nimi":"360 led-360 led-yksipäinen-150","maara":23,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":70,"nimi":"360 led-360 led-yksipäinen-100","maara":40,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":71,"nimi":"RGB wash pixel ohjattu","maara":30,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":72,"nimi":"trussi paketti","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":73,"nimi":"Loossi","maara":10,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":74,"nimi":"Päätylaatta-päätylaatta (eurotruss)","maara":2,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":75,"nimi":"Päätylaatta-päätylaatta (alutruss)","maara":8,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":76,"nimi":"Päätylaatta-päätylaatta (milos)","maara":3,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":77,"nimi":"Päätylaatta-päätylaatta (globaltruss/omavalmiste)","maara":2,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":78,"nimi":"Päätylaatta-päätylaatta 60x60cm rauta (musta) (globaltrus)","maara":4,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":79,"nimi":"Päätylaatta-päätylaatta 60x60cm alumiini (bt-truss)","maara":4,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":80,"nimi":"Päätylaatta","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":81,"nimi":"Trussit-Trussit-0,5m trussi","maara":4,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":82,"nimi":"Trussit-Trussit-1m trussi","maara":8,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":83,"nimi":"Trussit-Trussit-1,5m trussi","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":84,"nimi":"Trussit-Trussit-2m trussi","maara":16,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":85,"nimi":"Trussit-Trussit-2,5m trussi","maara":7,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":86,"nimi":"Trussit-Trussit-3m trussi","maara":24,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":87,"nimi":"Trussit-Trussit-3,5m trussi","maara":2,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":88,"nimi":"Trussit-Trussit-4m trussi","maara":12,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":89,"nimi":"Trussit-Trussit-4,5m trussi","maara":4,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":90,"nimi":"Trussit-Trussit-5m trussi","maara":2,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":91,"nimi":"Trussit","maara":0,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":92,"nimi":"2D kulma L","maara":23,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":93,"nimi":"3D kulma","maara":1,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":94,"nimi":"4D risteys","maara":4,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":95,"nimi":"t-pala","maara":3,"kategoria":"Piilotetut tuotteet","naytto":false},
  {"id":96,"nimi":"Lisätuote","maara":1000,"kategoria":"Piilotetut tuotteet","naytto":false}
];

function TuoteLista() {
  // Suodatetaan näkyvät tuotteet
  const naytettavat = tuotteet.filter(t => t.naytto);

  // Ryhmitellään tuotteet kategorioittain
  const ryhmitelty = naytettavat.reduce((acc, tuote) => {
    if (!acc[tuote.kategoria]) acc[tuote.kategoria] = [];
    acc[tuote.kategoria].push(tuote);
    return acc;
  }, {});

  return (
    <div>
      {Object.entries(ryhmitelty).map(([kategoria, tuotteet]) => (
        <div key={kategoria} style={{ marginBottom: "1.5em" }}>
          <h2>{kategoria}</h2>
          <ul>
            {tuotteet.map(tuote => (
              <li key={tuote.id}>
                {tuote.nimi} (määrä: {tuote.maara})
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default TuoteLista;
