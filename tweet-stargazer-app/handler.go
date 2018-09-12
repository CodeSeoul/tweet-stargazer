package function

import (
	"encoding/json"
	"github.com/s8sg/faasflow"
)

// Define provide definiton of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	flow.
		Apply("github-star", faasflow.Sync).
		Modify(func(data []byte) ([]byte, error) {
			event := map[string]string{}
			json.Unmarshal(data, &event)
			context.Set("login_name", event["login_name"])
			context.Set("repo_name", event["repo_name"])

			avatarReq := map[string]string{"avatar_url": event["avatar_url"]}
			data, _ = json.Marshal(avatarReq)
			return data, nil
		}).
		Apply("get-avatar", faasflow.Sync).
		Modify(func(data []byte) ([]byte, error) {
			avatar := map[string]string{}
			json.Unmarshal(data, &avatar)

			context.Set("contentType", avatar["contentType"])

			return []byte(avatar["content"]), nil
		}).
		Apply("polaroid", faasflow.Sync).
		Modify(func(data []byte) ([]byte, error) {
			gazerReq := map[string]string{}
			temp, _ := context.Get("login_name")
			gazerReq["login"], _ = temp.(string)
			temp, _ = context.Get("repo_name")
			gazerReq["repository"], _ = temp.(string)
			temp, _ = context.Get("contentType")
			gazerReq["contentType"] = temp.(string)

			gazerReq["image"] = string(data)

			data, _ = json.Marshal(gazerReq)
			return data, nil
		}).
		Apply("tweet-stargazer", faasflow.Sync).
		Modify(func(data []byte) ([]byte, error) {
			response := map[string]string{}
			response["tweet_result"] = string(data)
			response["status"] = "success"
			temp, _ := context.Get("login_name")
			response["username"], _ = temp.(string)
			temp, _ = context.Get("repo_name")
			response["repository"], _ = temp.(string)

			data, _ = json.Marshal(response)
			return data, nil
		}).
		OnFailure(func(err error) ([]byte, error) {
			response := map[string]string{}
			response["error"] = err.Error()
			response["status"] = "failure"
			temp, _ := context.Get("login_name")
			response["username"], _ = temp.(string)
			temp, _ = context.Get("repo_name")
			response["repository"], _ = temp.(string)

			data, _ := json.Marshal(response)
			return data, nil
		})
	return
}
