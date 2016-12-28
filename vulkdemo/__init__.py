import os.path
import numpy as np

from vulk.baseapp import BaseApp
from vulkbare import load_image
from vulk import vulkanconstant as vc
from vulk.vulkanobject import ShaderModule, Pipeline, PipelineShaderStage, \
        PipelineVertexInputState, PipelineViewportState, Viewport, Rect2D, \
        Offset2D, Extent2D, PipelineInputAssemblyState, \
        PipelineRasterizationState, PipelineMultisampleState, \
        PipelineColorBlendAttachmentState, PipelineColorBlendState, \
        AttachmentDescription, SubpassDescription, AttachmentReference, \
        SubpassDependency, Renderpass, CommandPool, Framebuffer, \
        ClearColorValue, Semaphore, SubmitInfo, submit_to_graphic_queue, \
        immediate_buffer, HighPerformanceBuffer, \
        VertexInputBindingDescription, VertexInputAttributeDescription, \
        DescriptorSetLayoutBinding, DescriptorSetLayout, DescriptorPool, \
        DescriptorBufferInfo, WriteDescriptorSet, update_descriptorsets, \
        PipelineLayout, DescriptorPoolSize, HighPerformanceImage, \
        ImageSubresourceRange, ImageView, Sampler, DescriptorImageInfo


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        path = os.path.dirname(os.path.abspath(__file__))
        w = self.context.width
        h = self.context.height

        # ----------
        # VERTEX BUFFER
        va = [([-0.5, -0.5], [1, 0, 0], [0, 0]),
              ([-0.5, 0.5], [0, 1, 0], [0, 1]),
              ([0.5, 0.5], [0, 0, 1], [1, 1]),
              ([0.5, -0.5], [1, 1, 1], [1, 0])]

        vertices = np.array(va, dtype='2float32, 3uint32, 2float32')
        vbuffer = HighPerformanceBuffer(self.context, vertices.nbytes,
                                        vc.BufferUsage.VERTEX_BUFFER)
        with vbuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, vertices.view(dtype=np.uint8), casting='no')

        # ----------
        # INDEX BUFFER
        ia = [0, 1, 2, 0, 2, 3]
        indices = np.array(ia, dtype=np.uint16)
        ibuffer = HighPerformanceBuffer(self.context, indices.nbytes,
                                        vc.BufferUsage.INDEX_BUFFER)
        with ibuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, indices.view(dtype=np.uint8), casting='no')

        # ----------
        # UNIFORM BUFFER
        ua = [1]
        uniforms = np.array(ua, dtype=np.float32)
        ubuffer = HighPerformanceBuffer(self.context, uniforms.nbytes,
                                        vc.BufferUsage.UNIFORM_BUFFER)
        with ubuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, uniforms.view(dtype=np.uint8), casting='no')

        # ----------
        # LOAD BITMAP
        image_file = open(os.path.join(path, 'vulkan.png'), 'rb')
        bitmap, bwidth, bheight, bcomponents = load_image(image_file.read())

        # ----------
        # TEST TEXTURE
        texture = HighPerformanceImage(self.context, vc.ImageType.TYPE_2D,
                                       vc.Format.R8G8B8_UNORM, bwidth,
                                       bheight, 1, 1, 1,
                                       vc.SampleCount.COUNT_1)
        texture_range = ImageSubresourceRange(vc.ImageAspect.COLOR,
                                              0, 1, 0, 1)
        texture_view = ImageView(
            self.context, texture.final_image, vc.ImageViewType.TYPE_2D,
            vc.Format.R8G8B8_UNORM, texture_range)
        texture_sampler = Sampler(
            self.context, vc.Filter.LINEAR, vc.Filter.LINEAR,
            vc.SamplerMipmapMode.LINEAR, vc.SamplerAddressMode.REPEAT,
            vc.SamplerAddressMode.REPEAT, vc.SamplerAddressMode.REPEAT,
            0, True, 16, False, vc.CompareOp.ALWAYS, 0, 0,
            vc.BorderColor.INT_OPAQUE_BLACK, False)

        # ----------
        # FILL TEXTURE
        wrapbitmap = np.array(bitmap, copy=False)
        with texture.bind(self.context) as t:
            wrapper = np.array(t, copy=False)
            np.copyto(wrapper, wrapbitmap, casting='no')

        # ----------
        # SHADER MODULES
        path = os.path.join(path, 'shader')
        with open(os.path.join(path, "vert.spv"), 'rb') as f:
            spirv_vs = f.read()
        with open(os.path.join(path, "frag.spv"), 'rb') as f:
            spirv_fs = f.read()

        vs_module = ShaderModule(self.context, spirv_vs)
        fs_module = ShaderModule(self.context, spirv_fs)

        # ----------
        # FINAL IMAGE LAYOUT
        with immediate_buffer(self.context) as cmd:
            self.context.final_image.update_layout(
                cmd, vc.ImageLayout.UNDEFINED,
                vc.ImageLayout.TRANSFER_SRC_OPTIMAL,
                vc.PipelineStage.TOP_OF_PIPE,
                vc.PipelineStage.TOP_OF_PIPE,
                vc.Access.NONE, vc.Access.TRANSFER_READ
            )

        # ----------
        # RENDERPASS
        attachment = AttachmentDescription(
            self.context.final_image.format, vc.SampleCount.COUNT_1,
            vc.AttachmentLoadOp.CLEAR, vc.AttachmentStoreOp.STORE,
            vc.AttachmentLoadOp.DONT_CARE,
            vc.AttachmentStoreOp.DONT_CARE,
            vc.ImageLayout.COLOR_ATTACHMENT_OPTIMAL,
            vc.ImageLayout.TRANSFER_SRC_OPTIMAL)
        subpass = SubpassDescription([AttachmentReference(
            vc.ImageLayout.NONE, vc.ImageLayout.COLOR_ATTACHMENT_OPTIMAL)])
        dependency = SubpassDependency(
            vc.SUBPASS_EXTERNAL,
            vc.PipelineStage.COLOR_ATTACHMENT_OUTPUT, vc.Access.NONE, 0,
            vc.PipelineStage.COLOR_ATTACHMENT_OUTPUT,
            vc.Access.COLOR_ATTACHMENT_READ | vc.Access.COLOR_ATTACHMENT_WRITE
        )
        renderpass = Renderpass(self.context, [attachment], [subpass],
                                [dependency])

        # ----------
        # DESCRIPTORS
        ubo_descriptor = DescriptorSetLayoutBinding(
            0, vc.DescriptorType.UNIFORM_BUFFER, 1,
            vc.ShaderStage.FRAGMENT, None)
        texture_descriptor = DescriptorSetLayoutBinding(
            1, vc.DescriptorType.COMBINED_IMAGE_SAMPLER, 1,
            vc.ShaderStage.FRAGMENT, None)
        layout_bindings = [ubo_descriptor, texture_descriptor]
        descriptor_layout = DescriptorSetLayout(self.context, layout_bindings)

        pool_sizes = [
            DescriptorPoolSize(vc.DescriptorType.UNIFORM_BUFFER, 1),
            DescriptorPoolSize(vc.DescriptorType.COMBINED_IMAGE_SAMPLER, 1)
        ]
        descriptor_pool = DescriptorPool(self.context, pool_sizes, 1)

        descriptor_set = descriptor_pool.allocate_descriptorsets(
            self.context, 1, [descriptor_layout])[0]

        descriptorbuffer_info = DescriptorBufferInfo(
            ubuffer.final_buffer, 0, 4)
        descriptorimage_info = DescriptorImageInfo(
            texture_sampler, texture_view,
            vc.ImageLayout.SHADER_READ_ONLY_OPTIMAL)

        descriptor_ubo_write = WriteDescriptorSet(
            descriptor_set, 0, 0, vc.DescriptorType.UNIFORM_BUFFER,
            [descriptorbuffer_info])
        descriptor_image_write = WriteDescriptorSet(
            descriptor_set, 1, 0, vc.DescriptorType.COMBINED_IMAGE_SAMPLER,
            [descriptorimage_info])

        update_descriptorsets(
            self.context, [descriptor_ubo_write, descriptor_image_write], [])

        # ----------
        # PIPELINE
        stages = [PipelineShaderStage(vs_module, vc.ShaderStage.VERTEX),
                  PipelineShaderStage(fs_module, vc.ShaderStage.FRAGMENT)]

        vertex_description = VertexInputBindingDescription(
            0, 28, vc.VertexInputRate.VERTEX)
        position_attribute = VertexInputAttributeDescription(
            0, 0, vc.Format.R32G32_SFLOAT, 0)
        color_attribute = VertexInputAttributeDescription(
            1, 0, vc.Format.R32G32B32_UINT, 8)
        texture_attribute = VertexInputAttributeDescription(
            2, 0, vc.Format.R32G32_SFLOAT, 20)
        vertex_input = PipelineVertexInputState([vertex_description],
                                                [position_attribute,
                                                 color_attribute,
                                                 texture_attribute])

        input_assembly = PipelineInputAssemblyState(
            vc.PrimitiveTopology.TRIANGLE_LIST)

        viewport_state = PipelineViewportState(
            [Viewport(0, 0, w, h, 0, 1)],
            [Rect2D(Offset2D(0, 0), Extent2D(w, h))])

        rasterization = PipelineRasterizationState(
            False, vc.PolygonMode.FILL, 1, vc.CullMode.BACK,
            vc.FrontFace.COUNTER_CLOCKWISE, 0, 0, 0)

        multisample = PipelineMultisampleState(
            False, vc.SampleCount.COUNT_1, 0)
        depth = None
        blend_attachment = PipelineColorBlendAttachmentState(
            False, vc.BlendFactor.ONE, vc.BlendFactor.ZERO,
            vc.BlendOp.ADD, vc.BlendFactor.ONE, vc.BlendFactor.ZERO,
            vc.BlendOp.ADD, vc.ColorComponent.R | vc.ColorComponent.G | vc.ColorComponent.B | vc.ColorComponent.A # noqa
        )
        blend = PipelineColorBlendState(False, vc.LogicOp.COPY,
                                        [blend_attachment], [0, 0, 0, 0])
        dynamic = None

        pipeline_layout = PipelineLayout(self.context, [descriptor_layout])

        pipeline = Pipeline(
            self.context, stages, vertex_input, input_assembly,
            viewport_state, rasterization, multisample, depth,
            blend, dynamic, pipeline_layout, renderpass)

        # ----------
        # COMMAND BUFFER
        commandpool = CommandPool(
            self.context, self.context.queue_family_indices['graphic'])
        commandbuffers = commandpool.allocate_buffers(
            self.context, vc.CommandBufferLevel.PRIMARY, 1)

        framebuffer = Framebuffer(self.context, renderpass,
                                  [self.context.final_image_view], w, h, 1)

        with commandbuffers[0].bind() as cmd:
            # We have to put the good layout because renderpass cannot do it
            # for us, it doesn't know the old layout of the image
            self.context.final_image.update_layout(
                cmd, vc.ImageLayout.TRANSFER_SRC_OPTIMAL,
                vc.ImageLayout.COLOR_ATTACHMENT_OPTIMAL,
                vc.PipelineStage.TOP_OF_PIPE,
                vc.PipelineStage.TOP_OF_PIPE,
                vc.Access.TRANSFER_READ,
                vc.Access.COLOR_ATTACHMENT_WRITE
            )

            # RenderPass manages the final_image dst layout
            cmd.begin_renderpass(
                renderpass,
                framebuffer,
                Rect2D(Offset2D(0, 0), Extent2D(w, h)),
                [ClearColorValue(float32=[0, 0, 1, 1])]
            )

            cmd.bind_pipeline(pipeline)
            cmd.bind_vertex_buffers(0, 1, [vbuffer.final_buffer], [0])
            cmd.bind_index_buffer(ibuffer.final_buffer, 0,
                                  vc.IndexType.UINT16)
            cmd.bind_descriptor_sets(pipeline_layout, 0, [descriptor_set], [])
            cmd.draw_indexed(6, 0)
            cmd.end_renderpass()

        # ----------
        # SUBMIT
        self.draw_semaphore = Semaphore(self.context)
        self.submit = SubmitInfo([], [], [self.draw_semaphore], commandbuffers) # noqa

    def end(self):
        pass

    def render(self, delta):
        submit_to_graphic_queue(self.context, [self.submit])
        self.context.swap([self.draw_semaphore])
