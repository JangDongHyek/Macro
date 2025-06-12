from JayGame import Game
import cv2
game = Game("gameTitle")

game.threadStart('mainKey',target=game.mainKey)
while True:
    if game._status:
        game.cameraStart()
        # game.threadStart("exam", target=game.onnxSearch, args=("exam",))
        while game._status :
            frame = game._camera.get_latest_frame()

            if frame is not None:
                game._frame = frame.copy()
                mouse = game.getMousePosition()
                game.drawText('mouse_x', "x : " + str(mouse[0]), (1700, 80))
                game.drawText('mouse_y', "y : " + str(mouse[1]), (1700, 100))

                # logic start

                # logic end

                game.drawFrame(frame)
                resized = cv2.resize(frame, (1024, 768))
                cv2.imshow("CCTV View", resized)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()
    else :
        if any(v for k, v in game._flags.items() if k != "mainKey"):
            game.threadAllStop()
        if game._camera_state:
            game.cameraStop()

    game.timeDelay()