local function make(trig_key, trig_translator)
    local flag = false

    local focus_text = nil
    local selected_candidate = nil
    local max_quality = nil

    local function processor(key, env)
        local kAccepted = 1
        local kNoop = 2
        local engine = env.engine
        local context = engine.context

        if key:repr() == trig_key then
            if context:is_composing() then
                focus_text = context:get_commit_text()
                selected_candidate = context:get_selected_candidate()
                local seg = context.composition:back()
                local first_cand = context.composition:back().menu:get_candidate_at(0)
                if first_cand ~= nil then
                    max_quality = first_cand.quality
                else
                    max_quality = nil
                end

                flag = true
                context:refresh_non_confirmed_composition()
                return kAccepted
            end
        end

        return kNoop
    end

    local function translator(input, seg, env)
        if flag then
            flag = false
            env.focus_text = focus_text
            env.selected_candidate = selected_candidate
            env.max_quality = max_quality
            trig_translator(input, seg, env)
            env.focus_text = nil
            env.selected_candidate = nil
            env.max_quality = nil
        end
    end

    return {
        processor = processor,
        translator = translator,
    }
end

return make
