import { FrameToStream, createEvent } from "../../../core/client/client.js";
import { segment } from "oicq";

export const rule = {
  life_restart: {
    reg: "^#人生重启",
    priority: 700,
    describe: "查询支持的所有插件",
  },
};

export async function life_restart(e) {
  FrameToStream({
    _package: "life_restart",
    _handler: "restart",
    params: {
      event: await createEvent(e),
    },
    onData: (error, response) => {
      if (error) {
        console.log(error.stack);
      } else {
        let msg = [response.message];
        if (response.messageDict.at) {
          msg.push(segment.at(response.messageDict.at));
        }

        if (response.image) {
          msg.push(segment.image(response.image));
        }
        e.reply(msg);
      }
    },
  });
}