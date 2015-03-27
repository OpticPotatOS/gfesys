# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from spirit.utils.ratelimit.decorators import ratelimit
from spirit.utils.decorators import moderator_required
from spirit.models.category import Category
from spirit.models.comment import MOVED, CLOSED, UNCLOSED, PINNED, UNPINNED
from spirit.forms.comment import CommentForm
from spirit.forms.topic_other import TopicOtherForm
from spirit.signals.comment import comment_posted
from spirit.forms.topic_poll import TopicPollForm, TopicPollChoiceFormSet

from spirit.models.topic import Topic
from spirit.forms.topic import TopicForm
from spirit.signals.topic import topic_viewed, topic_post_moderate


@login_required
@ratelimit(rate='1/10s')
def other_publish(request, other_type_id, other_object_id):
    if request.method == 'POST':
        form = TopicOtherForm(user=request.user, data=request.POST,other_category_id=other_object_id, other_category_content_type=other_type_id)
        cform = CommentForm(user=request.user, data=request.POST)
        pform = TopicPollForm(data=request.POST)
        pformset = TopicPollChoiceFormSet(can_delete=False, data=request.POST)

        if not request.is_limited and form.is_valid() and cform.is_valid() \
                and pform.is_valid() and pformset.is_valid():
            # wrap in transaction.atomic?
            topic = form.save()

            cform.topic = topic
            comment = cform.save()
            comment_posted.send(sender=comment.__class__, comment=comment, mentions=cform.mentions)

            # Create a poll only if we have choices
            if pformset.is_filled():
                pform.topic = topic
                poll = pform.save()
                pformset.instance = poll
                pformset.save()

            return redirect(topic.get_absolute_url())
    else:
        form = TopicOtherForm(user=request.user, other_category_id=other_object_id, other_category_content_type=other_type_id, initial={'category': 0})
        cform = CommentForm()
        pform = TopicPollForm()
        pformset = TopicPollChoiceFormSet(can_delete=False)

    return render(request, 'spirit/topic/topic_publish.html', {'form': form, 'cform': cform,
                                                               'pform': pform, 'pformset': pformset})


# @login_required
# def topic_update(request, pk):
    # topic = Topic.objects.for_update_or_404(pk, request.user)

    # if request.method == 'POST':
        # form = TopicForm(user=request.user, data=request.POST, instance=topic)
        # category_id = topic.category_id

        # if form.is_valid():
            # topic = form.save()

            # if topic.category_id != category_id:
                # topic_post_moderate.send(sender=topic.__class__, user=request.user, topic=topic, action=MOVED)

            # return redirect(request.POST.get('next', topic.get_absolute_url()))
    # else:
        # form = TopicForm(user=request.user, instance=topic)

    # return render(request, 'spirit/topic/topic_update.html', {'form': form, })


# def topic_detail(request, pk, slug):
    # topic = Topic.objects.get_public_or_404(pk, request.user)

    # if topic.slug != slug:
        # return HttpResponsePermanentRedirect(topic.get_absolute_url())

    # topic_viewed.send(sender=topic.__class__, request=request, topic=topic)

    # return render(request, 'spirit/topic/topic_detail.html', {'topic': topic,
                                                              # 'COMMENTS_PER_PAGE': settings.ST_COMMENTS_PER_PAGE})


# @moderator_required
# def topic_moderate(request, pk, value, remove=False, lock=False, pin=False):
    # # TODO: move to topic_moderate and split it in many views
    # topic = get_object_or_404(Topic, pk=pk)

    # if request.method == 'POST':
        # not_value = not value

        # if remove:
            # Topic.objects.filter(pk=pk, is_removed=not_value)\
                # .update(is_removed=value)

        # if lock:
            # count = Topic.objects.filter(pk=pk, is_closed=not_value)\
                # .update(is_closed=value)

            # if count:
                # action = CLOSED if value else UNCLOSED
                # topic_post_moderate.send(sender=topic.__class__, user=request.user, topic=topic, action=action)

        # if pin:
            # count = Topic.objects.filter(pk=pk, is_pinned=not_value)\
                # .update(is_pinned=value)

            # if count:
                # action = PINNED if value else UNPINNED
                # topic_post_moderate.send(sender=topic.__class__, user=request.user, topic=topic, action=action)

        # return redirect(request.POST.get('next', topic.get_absolute_url()))

    # return render(request, 'spirit/topic/topic_moderate.html', {'topic': topic, })


# def topics_active(request):
    # topics = Topic.objects.for_public().filter(is_pinned=False)
    # topics_pinned = Topic.objects.filter(category_id=settings.ST_UNCATEGORIZED_CATEGORY_PK,
                                         # is_removed=False,
                                         # is_pinned=True)
    # topics = topics | topics_pinned
    # topics = topics.order_by('-is_pinned', '-last_active').select_related('category')
    # categories = Category.objects.for_parent()

    # return render(request, 'spirit/topic/topics_active.html', {'categories': categories,
                                                               # 'topics': topics})