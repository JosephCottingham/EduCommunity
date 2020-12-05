$(document).ready(function () {

    // socket = io.connect(community_info.socketio_endpoint, {secure:false});
    socket = io.connect("http://127.0.0.1:5000/text_channel", {
        secure: false
    });


    socket.on('connect', function () {
        socket.emit('joined', {
            message: {
                channel_code: community_info.channel_code
            }
        });
    });

    socket.on('joined', function () {});

    socket.on('status', function (data) {
        // $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        // $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    socket.on('message', function (data) {
        if (community_info.user_code == data.msg.user.code){
            populate_user_message(data.msg[index])
        } else {
            populate_other_user_message(data.msg)
        }
    });

    socket.on('messages', function (data) {
        console.log(data);
        for(index = 0; index < Object.keys(data.msgs).length; index++) {

            if (community_info.user_code == data.msgs[index].user.code){
                populate_user_message(data.msgs[index])
            } else {
                populate_other_user_message(data.msgs[index])
            }
        }
        // $('#chat').val($('#chat').val() + data.msg + '\n');
        // $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    $('#text').keypress(function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {
                msg: text
            });
        }
    });

    function populate_other_user_message (msg) {
        var messagesEl = KTUtil.getById("messages-list");
        var scrollEl = KTUtil.getById("msg-scroller");

        var node = document.createElement("DIV");
			KTUtil.addClass(node, 'd-flex flex-column mb-5 align-items-start');

			var html = '';
			html += '<div class="d-flex align-items-center">';
            html += '	<div class="symbol symbol-circle symbol-40 mr-3">';
			html += '		<img alt="Pic" src="' + community_info.avatar_url.replace("USER_CODE",msg.user.code) + '"/>';
			html += '	</div>';
			html += '	<div>';
			html += '		<a href="#" class="text-dark-75 text-hover-primary font-weight-bold font-size-h6">' + msg.user.name + '</a>';
			html += '		<span class="text-muted font-size-sm">' + new Date(Date.parse(msg.time)).toLocaleString() + '</span>';
			html += '	</div>';
			html += '</div>';
			html += '<div class="mt-2 rounded p-5 bg-light-success text-dark-50 font-weight-bold font-size-lg text-left max-w-400px">';
			html += msg.text;
			html += '</div>';

			KTUtil.setHTML(node, html);
			messagesEl.appendChild(node);
			scrollEl.scrollTop = parseInt(KTUtil.css(messagesEl, 'height'));

			var ps;
			if (ps = KTUtil.data(scrollEl).get('ps')) {
				ps.update();
			}
    }

    function populate_user_message (msg) {
        var messagesEl = KTUtil.getById("messages-list");
        var scrollEl = KTUtil.getById("msg-scroller");

        var node = document.createElement("DIV");
        KTUtil.addClass(node, 'd-flex flex-column mb-5 align-items-end');

        var html = '';
        html += '<div class="d-flex align-items-center">';
        html += '	<div>';
        html += '		<span class="text-muted font-size-sm">' + new Date(Date.parse(msg.time)).toLocaleString() + '</span>';
        html += '		<a href="#" class="text-dark-75 text-hover-primary font-weight-bold font-size-h6">' + msg.user.name + '</a>';
        html += '	</div>';
        html += '	<div class="symbol symbol-circle symbol-40 ml-3">';
        html += '		<img alt="Pic" src="' + community_info.avatar_url.replace("USER_CODE",msg.user.code) + '"/>';
        html += '	</div>';
        html += '</div>';
        html += '<div class="mt-2 rounded p-5 bg-light-primary text-dark-50 font-weight-bold font-size-lg text-right max-w-400px">' + msg.text + '</div>';


        KTUtil.setHTML(node, html);
        messagesEl.appendChild(node);
        scrollEl.scrollTop = parseInt(KTUtil.css(messagesEl, 'height'));

        var ps;
        if (ps = KTUtil.data(scrollEl).get('ps')) {}
    }


    // Class definition
    var KTLayoutChat = function () {
        // Private functions
        var _init = function (element) {
            var scrollEl = KTUtil.find(element, '.scroll');
            var cardBodyEl = KTUtil.find(element, '.card-body');
            var cardHeaderEl = KTUtil.find(element, '.card-header');
            var cardFooterEl = KTUtil.find(element, '.card-footer');

            if (!scrollEl) {
                return;
            }

            // initialize perfect scrollbar(see:  https://github.com/utatti/perfect-scrollbar)
            KTUtil.scrollInit(scrollEl, {
                windowScroll: false, // allow browser scroll when the scroll reaches the end of the side
                mobileNativeScroll: true, // enable native scroll for mobile
                desktopNativeScroll: false, // disable native scroll and use custom scroll for desktop
                resetHeightOnDestroy: true, // reset css height on scroll feature destroyed
                handleWindowResize: true, // recalculate hight on window resize
                rememberPosition: true, // remember scroll position in cookie
                height: function () { // calculate height
                    var height;

                    if (KTUtil.isBreakpointDown('lg')) { // Mobile mode
                        return KTUtil.hasAttr(scrollEl, 'data-mobile-height') ? parseInt(KTUtil.attr(scrollEl, 'data-mobile-height')) : 400;
                    } else if (KTUtil.isBreakpointUp('lg') && KTUtil.hasAttr(scrollEl, 'data-height')) { // Desktop Mode
                        return parseInt(KTUtil.attr(scrollEl, 'data-height'));
                    } else {
                        height = KTLayoutContent.getHeight();

                        if (scrollEl) {
                            height = height - parseInt(KTUtil.css(scrollEl, 'margin-top')) - parseInt(KTUtil.css(scrollEl, 'margin-bottom'));
                        }

                        if (cardHeaderEl) {
                            height = height - parseInt(KTUtil.css(cardHeaderEl, 'height'));
                            height = height - parseInt(KTUtil.css(cardHeaderEl, 'margin-top')) - parseInt(KTUtil.css(cardHeaderEl, 'margin-bottom'));
                        }

                        if (cardBodyEl) {
                            height = height - parseInt(KTUtil.css(cardBodyEl, 'padding-top')) - parseInt(KTUtil.css(cardBodyEl, 'padding-bottom'));
                        }

                        if (cardFooterEl) {
                            height = height - parseInt(KTUtil.css(cardFooterEl, 'height'));
                            height = height - parseInt(KTUtil.css(cardFooterEl, 'margin-top')) - parseInt(KTUtil.css(cardFooterEl, 'margin-bottom'));
                        }
                    }

                    // Remove additional space
                    height = height - 2;

                    return height;
                }
            });

            // attach events
            KTUtil.on(element, '.card-footer textarea', 'keydown', function (e) {
                if (e.keyCode == 13) {
                    _handeMessaging(element);
                    e.preventDefault();

                    return false;
                }
            });

            KTUtil.on(element, '.card-footer .chat-send', 'click', function (e) {
                _handeMessaging(element);
            });
        }

        var _handeMessaging = function (element) {
            var messagesEl = KTUtil.find(element, '.messages');
            var scrollEl = KTUtil.find(element, '.scroll');
            var textarea = KTUtil.find(element, 'textarea');

            if (textarea.value.length === 0) {
                return;
            }
            var node = document.createElement("DIV");
            KTUtil.addClass(node, 'd-flex flex-column mb-5 align-items-end');

            socket.emit('msg', {
                'message': {
                    text: textarea.value,
                    channel_code: community_info.channel_code,
                }
            });

            var html = '';
            html += '<div class="d-flex align-items-center">';
            html += '	<div>';
            html += '		<span class="text-muted font-size-sm">' + new Date().getTime().toString() + '</span>';
            html += '		<a href="#" class="text-dark-75 text-hover-primary font-weight-bold font-size-h6">' + community_info.user_name + '</a>';
            html += '	</div>';
            html += '	<div class="symbol symbol-circle symbol-40 ml-3">';
            html += '		<img alt="Pic" src="' + community_info.avatar_url.replace("USER_CODE", community_info.user_code) + '"/>';
            html += '	</div>';
            html += '</div>';
            html += '<div class="mt-2 rounded p-5 bg-light-primary text-dark-50 font-weight-bold font-size-lg text-right max-w-400px">' + textarea.value + '</div>';


            KTUtil.setHTML(node, html);
            messagesEl.appendChild(node);
            textarea.value = '';
            scrollEl.scrollTop = parseInt(KTUtil.css(messagesEl, 'height'));

            var ps;
            if (ps = KTUtil.data(scrollEl).get('ps')) {}
        }

        // Public methods
        return {
            init: function () {
                // init modal chat example
                _init(KTUtil.getById('kt_chat_modal'));

                // trigger click to show popup modal chat on page load
                if (encodeURI(window.location.hostname) == 'keenthemes.com' || encodeURI(window.location.hostname) == 'www.keenthemes.com') {
                    setTimeout(function () {
                        if (!KTCookie.getCookie('kt_app_chat_shown')) {
                            var expires = new Date(new Date().getTime() + 60 * 60 * 1000); // expire in 60 minutes from now

                            KTCookie.setCookie('kt_app_chat_shown', 1, {
                                expires: expires
                            });

                            if (KTUtil.getById('kt_app_chat_launch_btn')) {
                                KTUtil.getById('kt_app_chat_launch_btn').click();
                            }
                        }
                    }, 2000);
                }
            },

            setup: function (element) {
                _init(element);
            }
        };
    }();

    "use strict";

    // Class definition
    var KTAppChat = function () {
        var _chatAsideEl;
        var _chatAsideOffcanvasObj;
        var _chatContentEl;

        // Private functions
        var _initAside = function () {
            // Mobile offcanvas for mobile mode
            _chatAsideOffcanvasObj = new KTOffcanvas(_chatAsideEl, {
                overlay: true,
                baseClass: 'offcanvas-mobile',
                //closeBy: 'kt_chat_aside_close',
                toggleBy: 'kt_app_chat_toggle'
            });

            // User listing
            var cardScrollEl = KTUtil.find(_chatAsideEl, '.scroll');
            var cardBodyEl = KTUtil.find(_chatAsideEl, '.card-body');
            var searchEl = KTUtil.find(_chatAsideEl, '.input-group');

            if (cardScrollEl) {
                // Initialize perfect scrollbar(see:  https://github.com/utatti/perfect-scrollbar)
                KTUtil.scrollInit(cardScrollEl, {
                    mobileNativeScroll: true, // Enable native scroll for mobile
                    desktopNativeScroll: false, // Disable native scroll and use custom scroll for desktop
                    resetHeightOnDestroy: true, // Reset css height on scroll feature destroyed
                    handleWindowResize: true, // Recalculate hight on window resize
                    rememberPosition: true, // Remember scroll position in cookie
                    height: function () { // Calculate height
                        var height;

                        if (KTUtil.isBreakpointUp('lg')) {
                            height = KTLayoutContent.getHeight();
                        } else {
                            height = KTUtil.getViewPort().height;
                        }

                        if (_chatAsideEl) {
                            height = height - parseInt(KTUtil.css(_chatAsideEl, 'margin-top')) - parseInt(KTUtil.css(_chatAsideEl, 'margin-bottom'));
                            height = height - parseInt(KTUtil.css(_chatAsideEl, 'padding-top')) - parseInt(KTUtil.css(_chatAsideEl, 'padding-bottom'));
                        }

                        if (cardScrollEl) {
                            height = height - parseInt(KTUtil.css(cardScrollEl, 'margin-top')) - parseInt(KTUtil.css(cardScrollEl, 'margin-bottom'));
                        }

                        if (cardBodyEl) {
                            height = height - parseInt(KTUtil.css(cardBodyEl, 'padding-top')) - parseInt(KTUtil.css(cardBodyEl, 'padding-bottom'));
                        }

                        if (searchEl) {
                            height = height - parseInt(KTUtil.css(searchEl, 'height'));
                            height = height - parseInt(KTUtil.css(searchEl, 'margin-top')) - parseInt(KTUtil.css(searchEl, 'margin-bottom'));
                        }

                        // Remove additional space
                        height = height - 2;

                        return height;
                    }
                });
            }
        }

        return {
            // Public functions
            init: function () {
                // Elements
                _chatAsideEl = KTUtil.getById('kt_chat_aside');
                _chatContentEl = KTUtil.getById('kt_chat_content');

                // Init aside and user list
                _initAside();

                // Init inline chat example
                KTLayoutChat.setup(KTUtil.getById('kt_chat_content'));

                // Trigger click to show popup modal chat on page load
                if (KTUtil.getById('kt_app_chat_toggle')) {
                    setTimeout(function () {
                        KTUtil.getById('kt_app_chat_toggle').click();
                    }, 1000);
                }
            }
        };
    }();
    KTAppChat.init();
});