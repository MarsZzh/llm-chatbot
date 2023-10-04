$(function () {
    $('#user-form').submit(function (event) {
        event.preventDefault();
        var user_input = $('#user-input-text').val();
        $('#messages').append('<div class="message user-message">' + user_input + '</div>');
        $('#messages').append('<div class="message bot-message">正在思考...</div>');


        $.ajax({
            type: 'POST',
            url: '/get_response',
            data: JSON.stringify({user_input: user_input, id:unique}),
            contentType: "application/json", //必须这样写POST   还要加JSON.stringify()
            success: function (response) {
                $('.bot-message:contains("正在思考...")').remove();
                $('#messages').append('<div class="message bot-message">' + response + '</div>');
                $('#messages').animate({scrollTop: $('#messages').prop("scrollHeight")}, 1000);
                $('pre code').each(function (i, block) {
                    hljs.highlightBlock(block);
                });

                loadAudioList();
            }
        });
        $('#user-input-text').val('');
    });

    // 点击Reset按钮时重置对话和更新user ID
    $('#reset-button').click(function () {
        $.ajax({
            type: 'GET',
            url: '/reset',
            success: function (response) {
                $('#messages').empty();
            }
        });
    });


    //生成n位数字字母混合字符串
    function generateMixed(n) {
        var chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        var res = "";
        for (var i = 0; i < n; i++) {
            var id = Math.floor(Math.random() * 36);
            res += chars[id];
        }
        return res;
    }

    const unique = generateMixed(7)


    const audioItemTemplate = document.getElementById('audio-item-template').content;

    function loadAudioList(callback) {

        // Fetch the JSON data
        fetch('static/json/barkwebui.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('JSON data file not found');
                }
                return response.json();
            })
            .then(data => {
                for (const key in data) {
                    if (data.hasOwnProperty(key)) {
                        const item = data[key];
                        const filename = item.outputFile;
                        const textInput = item.textInput;

                        // Create a new audio item using the template
                        const audioItem = audioItemTemplate.cloneNode(true);
                        audioItem.querySelector('.audio-player').src = 'static/output/' + filename;
                        al = document.getElementById('audio-list')
                        al.appendChild(audioItem);
                    }
                }
            })
            .catch(error => {
                if (error.message === 'JSON data file not found') {
                    console.log('barkwebui.json file does not exist');
                } else {
                    console.log('Error loading audio list:', error);
                }
            })
            .finally(() => {
                if (callback) callback();
            });
    }


    function downloadFile(url, filename) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.target = '_blank';
        link.click();
    }

    function deleteAudioFile(filename) {
        fetch('/static/output/' + filename, {method: 'DELETE'})
            .then(function () {
                // Refresh the audio list
                console.log('File deleted: ', filename);
            })
            .catch(function (error) {
                console.log('Error deleting file: ', error);
            });
    }


});
