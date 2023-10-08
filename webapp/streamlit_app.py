import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            
            <title>Music Lyrics Analyser - AI Powered</title>

            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
            <!-- Favicons -->
            <link rel="apple-touch-icon" href="https://getbootstrap.com/docs/5.0/assets/img/favicons/apple-touch-icon.png" sizes="180x180">
            <link rel="manifest" href="https://getbootstrap.com/docs/5.0/assets/img/favicons/manifest.json">
            <link rel="mask-icon" href="https://getbootstrap.com/docs/5.0/assets/img/favicons/safari-pinned-tab.svg" color="#7952b3">
            <link rel="icon" href="../static/icon.png">
            
            <meta name="theme-color" content="#7952b3">

            <!-- Custom styles for this template -->
            <link href="../static/index.css" rel="stylesheet">
        </head>

        <body class="text-center">
            <div class="modal" id="modal-loading" data-backdrop="static">
                <div class="modal-dialog modal-sm">
                <div class="modal-content">
                    <div class="modal-body text-center">
                    <div class="loading-spinner mb-2"></div>
                    <div>Loading</div>
                    </div>
                </div>
                </div>
            </div>
            <main class="form-signin" style="width: 1100px !important">
                <div class="text-center">
                    <img src="../static/logo.png" class="rounded" width="500" height="350">
                </div>
                <br>
                <br>
                <div class="form-floating" >
                    <div class="container">
                        <div class="row">
                            <div class="col-2">
                                <h6 class="text-left">Model Selection</h6>
                            </div>
                            <div class="col-10">
                                <h6>Lyrics</h6> 
                            </div>
                        </div>
                        <div class="row">
                            <div class="col w-30">
                                <select id="modelSelect" class="form-select" aria-label="Default select example">
                                    <option value="LR_ovr">Logistic Regression-OVR</option>
                                    <option value="LR_mn">Logistic Regression-Multinomial</option>
                                    <option value="NB_MN">Navie Bayes-Multinomial</option>
                                    <option value="SVC">Linear SVC</option>
                                    <option value="bert-base-uncased_v2">BERT</option>
                                    <option value="albert-large-v1_v2">ALBERT-v1</option>
                                    <option value="albert-large-v2">ALBERT-v2</option>
                                    <option value="distilbert-base-uncased_v2">DistilBERT</option>
                                    <option value="roberta-base_v2">RoBERTa</option>
                                </select>
                            </div>
                            <div class="col w-70">
                                <input type="text" class="form-control" placeholder="Type here..." id="lyricsField" style="width: 700px !important"> 
                            </div>
                        </div>
                    </div>
                    
                    
                </div>
                <br>
                <br>
                </div>
                <button class="w-100 btn btn-lg btn-primary" onclick="analyse()" type="button" style="width: 300px !important">Analyse</button>
                <br>
                <br>
                <div id="div_result" hidden>
                    <h1>Result</h1>
                    <h2>Predicted Emotion</h2>
                    <div class="card">
                        <div id="card_text" class="card-body">

                        </div>
                    </div>
                </div>
            
            </main>
            
            
            <div data-lastpass-root=""
                style="position: absolute !important; top: 0px !important; left: 0px !important; height: 0px !important; width: 0px !important;">
                <div data-lastpass-infield="true" style="position: absolute !important; top: 0px !important; left: 0px !important;">
                </div>
            </div>
        </body>

        <!-- Bootstrap JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
        <script>
            url = "http://127.0.0.1:5000";
            const model_select = "model_select";

            // password check using flask request using ajax and jquery
            async function analyse() {
                document.getElementById("div_result").hidden = true;
                var model_v = document.getElementById("modelSelect").value;
                var lyrics_v = document.getElementById("lyricsField").value;
                //password = "Password"
                console.log(url+"/"+model_select);
                $('#modal-loading').modal('show');
                await fetch(`${url}/${model_select}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        model_k: model_v,
                        lyrics_k: lyrics_v
                    }),
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data["data"]);
                    $('#modal-loading').modal('hide');
                    document.getElementById("card_text").innerHTML = data["data"];
                    document.getElementById("div_result").hidden = false;
                    return data;
                })
                .catch((error) => {
                    // Errors when calling the service; such as network error,
                    // service offline, etc
                    console.log(error);
                    $('#modal-loading').modal('hide');
                });
            }
        </script>
        </html>


    """,
    
height=600,
)