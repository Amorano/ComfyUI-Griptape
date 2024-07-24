/**
 * File: gtUIGenericConfig.js
 * Project: ComfyUI-Griptape
 *
 */

import { app } from "../../../scripts/app.js";
import { hideWidget, showWidget } from "./utils.js";

app.registerExtension({
    name: "comfy.gtUIGenericConfig",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "Griptape Agent Config: Multi-service Node") {
            return;
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated
        nodeType.prototype.onNodeCreated = function () {
            const me = onNodeCreated?.apply(this);
            const widget_service = this.widgets.find(w => w.name === 'service_model');
            const widget_prompt_model = this.widgets.find(w => w.name === 'prompt_model');
            // generic
            const widget_apikey = this.widgets.find(w => w.name === 'api_key_env_var');
            const widget_prompt_model_name = this.widgets.find(w => w.name === 'prompt_model_deployment_name');
            // azure
            const widget_azure = this.widgets.find(w => w.name === 'azure_endpoint_env_var');
            // amazon
            const widget_aws_key = this.widgets.find(w => w.name === 'aws_access_key_id_env_var');
            const widget_aws_secret = this.widgets.find(w => w.name === 'aws_secret_access_key_env_var');
            const widget_aws_region = this.widgets.find(w => w.name === 'aws_default_region_env_var');

            widget_service.callback = async () => {
                hideWidget(this, widget_apikey);
                hideWidget(this, widget_prompt_model_name);
                //
                hideWidget(this, widget_azure);
                //
                hideWidget(this, widget_aws_key);
                hideWidget(this, widget_aws_secret);
                hideWidget(this, widget_aws_region);

                switch (widget_service.value) {
                    case "amazon bedrock":
                        showWidget(widget_aws_key);
                        showWidget(widget_aws_secret);
                        showWidget(widget_aws_region);
                        break;

                    case "azure openai":
                        showWidget(widget_prompt_model_name);
                        showWidget(widget_apikey);
                        showWidget(widget_azure);
                        break;

                    default:
                        break;
                }
            }
            setTimeout(() => { widget_service.callback(); }, 5);
            return me;
        }
	}
})
